from __future__ import annotations
import os
from pathlib import Path
from typing import Optional, Dict, Any, List

# Robust adapter import: if OpenRouter missing, use a stub that triggers fallback.
try:
    from ..adapters import openrouter  # type: ignore
except Exception:  # pragma: no cover
    class _OpenRouterStub:
        @staticmethod
        def generate_reply(*_args: Any, **_kwargs: Any) -> str:
            raise NotImplementedError("openrouter adapter not available")
    openrouter = _OpenRouterStub()  # type: ignore

from .observability import new_trace_id, utc_now_iso, jsonl_logger, time_block
from .classifier import classify
from . import safety, rewrite, node_rules, schema, memory_tracker, style_engine, context, tokens, hx_engine, culture_shift
from .config import load

def _craft_prompt(user_input: str, emo: str, intent: str, ctx: List[dict], style_name: str) -> str:
    head = (
        "You are Babbel Core. Respond briefly and concretely.\n"
        f"Style profile: {style_name}\n"
        f"Emotion hint: {emo or '-'} | Intent hint: {intent or '-'}"
    )
    ctx_lines: List[str] = []
    if ctx:
        ctx_lines.append("Recent context:")
        for item in ctx:
            u = (item.get("user_input","") or "").strip().replace("\\n", " ")
            r = (item.get("response","") or "").strip().replace("\\n", " ")
            if u:
                ctx_lines.append(f"- U: {u[:140]}")
            if r:
                ctx_lines.append(f"  A: {r[:140]}")
    body = f"User said:\\n---\\n{user_input}\\n---"
    return "\\n".join(([head] + ctx_lines + [body]))

def _safety_message(reasons: List[str]) -> str:
    if "self_harm" in reasons:
        return (
            "I'm really sorry you're feeling this way. I can't help with that here. "
            "If you might be in immediate danger, please call your local emergency number now. "
            "If you can, consider reaching out to someone you trust or a local crisis hotline."
        )
    if "pii" in reasons:
        return "I can’t help with sharing or handling sensitive credentials. Let’s talk about safer alternatives."
    return "I can’t help with that. We can talk about safety and next steps if you want."

def process_message(user_input: str, user_id: Optional[str] = None) -> Dict[str, Any]:
    cfg = load()
    trace_id = new_trace_id()
    logger = jsonl_logger(Path(cfg.LOG_JSONL))

    # Classification
    with time_block("classify") as tb:
        c = classify(user_input)
    logger.write({"trace_id":trace_id, "step":"classify", "elapsed_ms":tb["elapsed_ms"], "out":c})

    # Early input safety
    with time_block("safety_input") as tb:
        input_scan = safety.analyze(user_input)
    logger.write({"trace_id":trace_id, "step":"safety_input", "elapsed_ms":tb["elapsed_ms"], "out":{k:input_scan[k] for k in ("blocked","reasons")}})
    if input_scan["blocked"]:
        guiding_line = "Decline unsafe request; offer safety-oriented next steps."
        final_text = _safety_message(input_scan["reasons"])
        payload = {
            "trace_id": trace_id,
            "guiding_line": guiding_line,
            "final_text": final_text,
            "emotion": (c["emotion"] or ""),
            "intent": (c["intent"] or ""),
            "notes": "input_safety_triggered",
            "tokens_used": None,
            "timestamp_utc": utc_now_iso(),
            "safety": {"blocked": True, "reasons": input_scan.get("reasons", [])},
            "ux": {
                "reflection": "Safety first.",
                "choices": [],
                "question": "Is there someone you can reach out to right now?",
                "cta": "Please contact local emergency services if you’re in danger.",
                "style_profile": cfg.STYLE_PROFILE,
                "culture_explanation": None,
            },
        }
        fp = schema.validate_payload(payload)
        with time_block("memory_log") as tb:
            memory_tracker.log_interaction(fp.emotion, fp.intent, user_input, fp.final_text)
        logger.write({"trace_id":trace_id, "step":"memory_log", "elapsed_ms":tb["elapsed_ms"]})
        logger.write({"trace_id":trace_id, "step":"return", "payload_keys": list(schema.to_dict(fp).keys())})
        return schema.to_dict(fp)

    # Context retrieval
    with time_block("context") as tb:
        ctx_items = context.get_recent(cfg.CONTEXT_ITEMS, cfg.MEMORY_FILE)
    logger.write({"trace_id":trace_id, "step":"context", "elapsed_ms":tb["elapsed_ms"], "count": len(ctx_items)})

    prompt = _craft_prompt(user_input, c["emotion"], c["intent"], ctx_items, cfg.STYLE_PROFILE)

    # Human-experience extras (precomputed for both fallback and real generations)
    hx_extras = hx_engine.build_extras(user_input, c["emotion"], c["intent"], cfg.STYLE_PROFILE)
    max_ux_items = max(1, min(3, int(os.environ.get("BABBEL_UX_ITEMS", "2"))))

    # Generate (or fallback)
    used_fallback = False
    try:
        with time_block("generate") as tb:
            raw = openrouter.generate_reply(prompt, cfg.MODEL_NAME, cfg.TIMEOUT_S)
        logger.write({"trace_id":trace_id, "step":"generate", "elapsed_ms":tb["elapsed_ms"]})
    except NotImplementedError:
        raw = None
    except Exception as e:  # pragma: no cover
        logger.write({"trace_id":trace_id, "step":"generate_error", "error": repr(e)})
        raw = None

    if raw is None:
        from .fallback import generate as fallback_generate
        with time_block("fallback") as tb:
            raw = fallback_generate(user_input, c["emotion"], c["intent"], cfg.STYLE_PROFILE, cfg.MAX_LINES)
        logger.write({"trace_id":trace_id, "step":"fallback", "elapsed_ms":tb["elapsed_ms"]})
        used_fallback = True

    # Output safety & shaping
    try:
        with time_block("safety_output") as tb:
            blocked, safety_dict, styled = safety.gate(raw)
        logger.write({"trace_id":trace_id, "step":"safety_output", "elapsed_ms":tb["elapsed_ms"], "out":safety_dict})
    except Exception as e:  # pragma: no cover
        logger.write({"trace_id":trace_id, "step":"safety_output_error", "error": repr(e)})
        blocked, safety_dict, styled = False, {"reasons": []}, raw

    if blocked:
        final_text = _safety_message(safety_dict.get("reasons", []))
        guiding_line = "Decline unsafe request; offer safety-oriented next steps."
    else:
        try:
            with time_block("rewrite") as tb:
                cleaned = rewrite.rewrite_response(styled or raw)
            logger.write({"trace_id":trace_id, "step":"rewrite", "elapsed_ms":tb["elapsed_ms"]})
        except Exception as e:  # pragma: no cover
            cleaned = styled or raw
            logger.write({"trace_id":trace_id, "step":"rewrite_error", "error": repr(e)})

        try:
            with time_block("style") as tb:
                profile = style_engine.from_config(cfg)
                shaped = style_engine.apply(cleaned, profile)
            logger.write({"trace_id":trace_id, "step":"style", "elapsed_ms":tb["elapsed_ms"], "profile": profile.name})
        except Exception as e:  # pragma: no cover
            shaped = cleaned
            profile = type("P", (), {"name": "default", "max_lines": 6})()  # lightweight stub
            logger.write({"trace_id":trace_id, "step":"style_error", "error": repr(e)})

        with time_block("node_rules") as tb:
            guided, guiding_line = node_rules.apply_node_rules(shaped, c["emotion"], c["intent"])
        logger.write({"trace_id":trace_id, "step":"node_rules", "elapsed_ms":tb["elapsed_ms"], "line":guiding_line})

        # If we used fallback, prefer the HX brief composition (more human-feeling)
        if used_fallback:
            hx_text = hx_engine.compose_brief(hx_extras, max_items=max_ux_items)
            final_text = hx_text
        else:
            final_text = guided

        # Optional culture shift (after shaping). Re-apply style caps if changed.
        target_culture = os.environ.get("BABBEL_TARGET_CULTURE", "").strip()
        culture_note = None
        if os.environ.get("BABBEL_CULTURE_SHIFT", "").strip() and target_culture:
            with time_block("culture_shift") as tb:
                adjusted, expl = culture_shift.apply_and_explain(final_text, target_culture)
            logger.write({"trace_id":trace_id, "step":"culture_shift", "elapsed_ms":tb["elapsed_ms"], "target": target_culture})
            if adjusted:
                try:
                    final_text = style_engine.apply(adjusted, profile)
                except Exception:
                    final_text = adjusted
            if expl:
                culture_note = expl

    try:
        tokens_used = tokens.rough_token_estimate(user_input, prompt, final_text)
    except Exception:  # pragma: no cover
        tokens_used = None

    ux_block = {
        "reflection": hx_extras.get("reflection"),
        "choices": (hx_extras.get("choices", []) or [])[:max_ux_items],
        "question": hx_extras.get("question"),
        "cta": hx_extras.get("cta"),
        "style_profile": cfg.STYLE_PROFILE,
        "culture_explanation": locals().get("culture_note"),
    }

    payload = {
        "trace_id": trace_id,
        "guiding_line": guiding_line,
        "final_text": final_text,
        "emotion": (c["emotion"] or ""),
        "intent": (c["intent"] or ""),
        "notes": ("fallback_reply" if used_fallback else None),
        "tokens_used": tokens_used,
        "timestamp_utc": utc_now_iso(),
        "safety": {"blocked": bool(blocked), "reasons": safety_dict.get("reasons", [])},
        "ux": ux_block,
    }

    fp = schema.validate_payload(payload)

    with time_block("memory_log") as tb:
        memory_tracker.log_interaction(fp.emotion, fp.intent, user_input, fp.final_text)
    logger.write({"trace_id":trace_id, "step":"memory_log", "elapsed_ms":tb["elapsed_ms"]})
    logger.write({"trace_id":trace_id, "step":"return", "payload_keys": list(schema.to_dict(fp).keys())})

    return schema.to_dict(fp)

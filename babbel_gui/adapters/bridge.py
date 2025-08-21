from babbel_core.engine import process_message

def get_babbel_response(
    text,
    *,
    show_metadata: bool,
    live_preview: bool,
    emotion_savvy: bool = False,
    emit_emotion_series: bool = False,
    cultural_sensitivity: bool = False,
    session=None,
):
    result = process_message(
        text=text, emotion_savvy=emotion_savvy,
        emit_emotion_series=emit_emotion_series,
        cultural_sensitivity=cultural_sensitivity,
        session=session,
    )
    return result

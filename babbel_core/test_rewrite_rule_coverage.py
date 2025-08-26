import os
from .node_rewrite_v2 import NodeRewriterV2

rewriter = NodeRewriterV2()
covered = []
unmatched = []

print("\n🎯 Testing coverage for all rewrite rules...\n")

for rule in rewriter.rewrite_rules:
    trigger = rule.get("trigger", "").strip()
    if not trigger:
        continue
    result = rewriter.rewrite_node(trigger)
    if result != trigger:
        covered.append(trigger)
    else:
        unmatched.append(trigger)

print("\n✅ COVERED TRIGGERS:")
for c in covered:
    print(f"  ✔ {c}")

print("\n❌ UNCOVERED TRIGGERS:")
for u in unmatched:
    print(f"  ✖ {u}")

print(f"\n📊 Coverage: {len(covered)}/{len(rewriter.rewrite_rules)} matched.\n")

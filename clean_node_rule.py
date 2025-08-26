#!/usr/bin/env python3

path = "babbel_core/node_rules.py"

with open(path) as f:
    lines = f.readlines()

# Remove broken top-level "return" line
lines = [l for l in lines if not l.strip().startswith('return "Let’s take one small step')]

# Inject the rewrite inside the function if not already present
target = 'def apply_node_rules(text, emotion, intent):'
new_line = '    if "stuck" in text.lower(): return "Let’s take one small step together and see where it leads."'

if not any("stuck" in l for l in lines):
    for i, line in enumerate(lines):
        if line.strip() == target.strip():
            lines.insert(i + 1, new_line + "\n")
            break

with open(path, "w") as f:
    f.writelines(lines)

print("✅ Cleaned node_rules.py and reinjected 'stuck' rule correctly.")

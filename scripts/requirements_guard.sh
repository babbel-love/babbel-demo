#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
import re, sys
from importlib import metadata as m
deny = re.compile(r'(?i)\b((c?hat)?gpt|open\s*ai)\b')
bad=[]
for d in m.distributions():
    name = d.metadata.get('Name','') or d.metadata.get('Summary','')
    fields = ' '.join([d.metadata.get(k,'') for k in ('Name','Summary','Home-page','Author','License')])
    text = f"{name} {fields}"
    if deny.search(text or ''):
        bad.append((d.metadata.get('Name',str(d)), d.metadata.get('Summary','')))
if bad:
    for n,s in bad:
        print(f"banned in dependency: {n} :: {s}")
    sys.exit(1)
print("requirements guard ok")
PY

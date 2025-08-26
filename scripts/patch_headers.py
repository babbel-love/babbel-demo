import os, re, sys
def patch(path):
    try:
        s = open(path, 'r', encoding='utf-8').read()
    except FileNotFoundError:
        return
    o = s
    s = s.replace('"HTTP-Referer"', '"Referer"')
    if '"Referer": _env_site(),' in s and '"Origin": _env_site(),' not in s:
        s = s.replace('"Referer": _env_site(),', '"Referer": _env_site(),\n        "Origin": _env_site(),')
    if 'os.getenv("OPENROUTER_SITE_URL' in s and '"Origin": os.getenv("OPENROUTER_SITE_URL' not in s:
        def add_origin(m):
            indent = m.group(1)
            return m.group(0) + "\n" + f'{indent}"Origin": os.getenv("OPENROUTER_SITE_URL","http://localhost:8501"),'
        s = re.sub(r'(^[ \t]*"Referer":\s*os\.getenv\("OPENROUTER_SITE_URL"[^)]*\),\s*$)', add_origin, s, flags=re.MULTILINE)
    s = re.sub(r'"X-Title":\s*"[^"]*"', '"X-Title": os.getenv("OPENROUTER_APP_TITLE","Babbel Local Dev")', s)
    if s != o:
        open(path, 'w', encoding='utf-8').write(s)
for p in sys.argv[1:]:
    patch(p)

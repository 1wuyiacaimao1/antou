import pathlib
import re

d = pathlib.Path(r"D:\hanacoagent\life-site\dist")
idx = (d / "index.html").read_text(encoding="utf-8")

for pat in ["/antou/assets/wood-grain", "/antou/fonts/LongCang", 'href="/antou/journal', 'href="/antou/lists']:
    print(pat, "->", idx.count(pat))

bad = sorted(set(re.findall(r'(?:href|src)="(/[^"]*)"', idx)))
print("root-absolute refs:", [b for b in bad if not b.startswith("/antou")][:10])

# 抽查子页面
sub = (d / "journal" / "index.html").read_text(encoding="utf-8")
print("journal back link ok:", 'href="/antou"' in sub)
print("journal item link ok:", 'href="/antou/journal/' in sub)

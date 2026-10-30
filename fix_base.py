import pathlib
import re

SRC = pathlib.Path(r"D:\hanacoagent\life-site\src")
BASE_LINE = "const base = import.meta.env.BASE_URL;"

for p in list(SRC.rglob("*.astro")):
    s = p.read_text(encoding="utf-8")
    if BASE_LINE not in s:
        continue

    # 先把可能放错位置的那一行全部拿掉
    s = s.replace("\n" + BASE_LINE, "").replace(BASE_LINE + "\n", "").replace(BASE_LINE, "")

    m = re.search(r"^---\n(.*?)\n---\n", s, re.S)
    if not m:
        print("skip (no frontmatter):", p.name)
        continue

    s = s[: m.end(1)] + "\n" + BASE_LINE + s[m.end(1) :]
    p.write_text(s, encoding="utf-8")
    print("fixed", p.relative_to(SRC))

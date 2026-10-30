import pathlib

SRC = pathlib.Path(r"D:\hanacoagent\life-site\src")
OLD = "const base = import.meta.env.BASE_URL;"
NEW = 'const base = import.meta.env.BASE_URL.replace(/\\/$/, "") + "/";'

for p in SRC.rglob("*.astro"):
    s = p.read_text(encoding="utf-8")
    if OLD in s:
        p.write_text(s.replace(OLD, NEW), encoding="utf-8")
        print("fixed", p.relative_to(SRC))

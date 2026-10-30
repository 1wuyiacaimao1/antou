import pathlib
import re

ROOT = pathlib.Path(r"D:\hanacoagent\life-site")
SRC = ROOT / "src"
report = []
BASE_LINE = "const base = import.meta.env.BASE_URL;"


def add_base_const(s):
    if BASE_LINE in s:
        return s
    m = re.search(r"^---\n(.*?)\n---\n", s, re.S)
    if not m:
        return s
    return s[: m.end(0)] + BASE_LINE + "\n" + s[m.end(0) :]


def edit(rel, pairs):
    p = SRC / rel
    s = p.read_text(encoding="utf-8")
    before = s
    for old, new in pairs:
        if old not in s:
            report.append("MISS " + rel + " :: " + old[:60])
        s = s.replace(old, new)
    s = add_base_const(s)
    if s != before:
        p.write_text(s, encoding="utf-8")
        report.append("ok   " + rel)


# ---------- Base 布局 ----------
p = SRC / "layouts" / "Base.astro"
s = p.read_text(encoding="utf-8")
if BASE_LINE not in s:
    s = s.replace(
        "const { title, description = \"随手记下的日子\" } = Astro.props;",
        "const { title, description = \"随手记下的日子\" } = Astro.props;\n" + BASE_LINE,
    )
s = s.replace(
    '<link rel="icon" href="/favicon.svg" type="image/svg+xml" />',
    '<link rel="icon" href={`${base}favicon.svg`} type="image/svg+xml" />',
)
if "--grain" not in s:
    s = s.replace(
        '<meta name="description" content={description} />',
        '<meta name="description" content={description} />\n'
        "    <style\n"
        "      is:inline\n"
        "      set:html={`:root{--grain:url(\"${base}assets/wood-grain.svg\")}\n"
        "@font-face{font-family:\"brush\";src:url(\"${base}fonts/LongCang.woff2\") format(\"woff2\");font-display:swap}`}\n"
        "    />",
    )
p.write_text(s, encoding="utf-8")
report.append("ok   layouts/Base.astro")

# ---------- 各页面链接 ----------
edit("pages/index.astro", [
    ("href={`/journal/${e.id}`}", "href={`${base}journal/${e.id}`}"),
    ('href="/journal"', "href={`${base}journal`}"),
    ('href="/moments"', "href={`${base}moments`}"),
    ('href="/lists"', "href={`${base}lists`}"),
    ('href="/notes"', "href={`${base}notes`}"),
    ('href="/bookmarks"', "href={`${base}bookmarks`}"),
    ("`/journal/${e.id}`", "`${base}journal/${e.id}`"),
])

edit("pages/journal/index.astro", [
    ('<a class="back" href="/">', "<a class=\"back\" href={base}>"),
    ("href={`/journal/${e.id}`}", "href={`${base}journal/${e.id}`}"),
])

edit("pages/journal/[...slug].astro", [
    ('<a class="back" href="/">', "<a class=\"back\" href={base}>"),
    ("href={`/journal/${prev.id}`}", "href={`${base}journal/${prev.id}`}"),
    ("href={`/journal/${next.id}`}", "href={`${base}journal/${next.id}`}"),
])

edit("pages/moments.astro", [
    ('<a class="back" href="/">', "<a class=\"back\" href={base}>"),
])

edit("pages/lists/index.astro", [
    ('<a class="back" href="/">', "<a class=\"back\" href={base}>"),
    ("href={`/lists/${l.id}`}", "href={`${base}lists/${l.id}`}"),
])

edit("pages/lists/[id].astro", [
    ('<a class="back" href="/">', "<a class=\"back\" href={base}>"),
])

edit("pages/notes.astro", [
    ('<a class="back-wood" href="/">', "<a class=\"back-wood\" href={base}>"),
])

edit("pages/bookmarks.astro", [
    ('<a class="back" href="/">', "<a class=\"back\" href={base}>"),
])

# ---------- 背景图改 CSS 变量 ----------
for rel in ["styles/site.css", "pages/index.astro", "pages/notes.astro"]:
    p = SRC / rel
    s = p.read_text(encoding="utf-8")
    n = s.count('url("/assets/wood-grain.svg")')
    s = s.replace('url("/assets/wood-grain.svg")', "var(--grain)")
    p.write_text(s, encoding="utf-8")
    report.append("grain " + rel + " :: " + str(n))

# ---------- 字体声明从 site.css 去掉 ----------
p = SRC / "styles" / "site.css"
s = p.read_text(encoding="utf-8")
s = re.sub(r"@font-face\{[^}]*\}\n\n", "", s, count=1)
p.write_text(s, encoding="utf-8")
report.append("font-face removed from site.css")

print("\n".join(report))

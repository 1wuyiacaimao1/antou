import pathlib
import subprocess

root = pathlib.Path(r"D:\hanacoagent\life-site")
dist = root / "dist"

css = [p for p in (dist / "_astro").glob("*.css")]
for p in css:
    t = p.read_text(encoding="utf-8")
    print(p.name, "len", len(t))
    print("  has var(--grain):", "--grain" in t or "var(--grain)" in t)
    print("  stale /assets/:", t.count("/assets/wood-grain"))

print("woff2 in dist:", list((dist / "fonts").glob("*")))
print("woff2 in public:", list((root / "public" / "fonts").glob("*")))

out = subprocess.run(["git", "ls-files"], cwd=root, capture_output=True, text=True).stdout
print("tracked woff2:", [l for l in out.splitlines() if "woff2" in l])

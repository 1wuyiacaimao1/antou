import pathlib
import re

d = pathlib.Path(r"D:\hanacoagent\life-site\dist")
idx = (d / "index.html").read_text(encoding="utf-8")

print("length", len(idx))
print("--- head style ---")
m = re.search(r"<style[^>]*>(.*?)</style>", idx, re.S)
print((m.group(1)[:400] if m else "NO STYLE"))

print("--- hrefs ---")
print(sorted(set(re.findall(r'href="([^"]+)"', idx)))[:12])

print("--- asset refs ---")
print(sorted(set(re.findall(r'(?:src|href)="([^"]*(?:assets|fonts)[^"]*)"', idx)))[:8])

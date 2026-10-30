"""把龙藏体按站内实际用到的字做成子集。
用法：python subset_font.py
扫 src/ 下所有 astro、ts、md，加上构建出来的 dist 里的文字，取并集。
"""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "src"
DIST = ROOT / "dist"
FULL = ROOT / "fonts" / "LongCang.ttf"
OUT = ROOT / "public" / "fonts" / "LongCang.woff2"

EXTRA = "0123456789.,-/:·×—…·「」『』（）《》！？、；："
extra_ascii = "".join(chr(c) for c in range(0x20, 0x7F))


def collect() -> str:
    chars = set(EXTRA) | set(extra_ascii)
    patterns = ["**/*.astro", "**/*.ts", "**/*.md"]
    for pat in patterns:
        for p in SRC.rglob(pat.split("/")[-1]):
            chars |= set(p.read_text(encoding="utf-8", errors="ignore"))
    if DIST.exists():
        for p in DIST.rglob("*.html"):
            chars |= set(p.read_text(encoding="utf-8", errors="ignore"))
    return "".join(sorted(chars))


def main():
    if not FULL.exists():
        print("找不到完整字体：", FULL)
        sys.exit(1)

    text = collect()
    OUT.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        sys.executable, "-m", "fontTools.subset", str(FULL),
        f"--text={text}",
        "--flavor=woff2",
        "--layout-features=*",
        "--desubroutinize",
        f"--output-file={OUT}",
    ]
    subprocess.run(cmd, check=True)

    kb = OUT.stat().st_size / 1024
    print(f"子集完成：{len(text)} 个字符 → {kb:.1f} KB")


if __name__ == "__main__":
    main()

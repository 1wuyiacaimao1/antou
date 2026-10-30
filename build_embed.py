"""把字体子集化并内联进 HTML，让 mock 文件双击即可打开，不受 file:// 字体跨域限制。"""
import base64
import io
import re
import sys
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = Path(__file__).parent
FONTS = ROOT / "fonts"

EXTRA = "0123456789.,-/:·×abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def chars_of(html_path: Path) -> str:
    text = html_path.read_text(encoding="utf-8")
    text = re.sub(r"<style.*?</style>", "", text, flags=re.S)
    text = re.sub(r"<script.*?</script>", "", text, flags=re.S)
    text = re.sub(r"<[^>]+>", "", text)
    return "".join(sorted(set(text) | set(EXTRA)))


def subset_woff2(src: Path, text: str) -> bytes:
    font = TTFont(str(src))
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.desubroutinize = True
    opts.layout_features = ["*"]
    opts.name_IDs = ["*"]
    opts.notdef_outline = True
    sub = subset.Subsetter(options=opts)
    sub.populate(text=text)
    sub.subset(font)
    buf = io.BytesIO()
    font.flavor = "woff2"
    font.save(buf)
    return buf.getvalue()


def embed(html_path: Path, mapping: dict[str, str]) -> None:
    text = chars_of(html_path)
    html = html_path.read_text(encoding="utf-8")
    for family, filename in mapping.items():
        data = subset_woff2(FONTS / filename, text)
        b64 = base64.b64encode(data).decode()
        uri = f"data:font/woff2;base64,{b64}"
        pattern = re.compile(
            r"(@font-face\s*\{[^}]*?font-family:\s*" + re.escape(family) + r";[^}]*?src:\s*)url\(\"[^\"]+\"\)(\s*format\(\"[^\"]+\"\))?",
            re.S,
        )
        html, n = pattern.subn(lambda m: m.group(1) + f'url("{uri}") format("woff2")', html, count=1)
        print(f"  {family}: {filename} -> {len(data)/1024:.1f} KB woff2, 替换 {n} 处")
    html_path.write_text(html, encoding="utf-8")
    print(f"  {html_path.name} 已内联，文件大小 {html_path.stat().st_size/1024:.0f} KB")


if __name__ == "__main__":
    targets = {
        "mock-c.html": {"brush": "MaShanZheng-Regular.ttf"},
        "compare.html": {
            "msz": "MaShanZheng-Regular.ttf",
            "lcb": "LongCang.ttf",
            "zmx": "ZhiMangXing.ttf",
            "kll": "ZCOOLKuaiLe.ttf",
            "kxw": "ZCOOLXiaoWei.ttf",
        },
    }
    for name, mapping in targets.items():
        p = ROOT / name
        if not p.exists():
            print(f"跳过 {name}")
            continue
        print(f"{name}:")
        embed(p, mapping)

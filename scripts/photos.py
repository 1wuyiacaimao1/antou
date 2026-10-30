"""把一个文件夹里的照片压成 webp，写进瞬间的内容文件。

用法：python scripts/photos.py "D:\某个文件夹"
"""
import datetime
import pathlib
import sys

from PIL import Image, ImageOps

try:
    import pillow_heif

    pillow_heif.register_heif_opener()
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT_ROOT = ROOT / "public" / "moments"
CONTENT = ROOT / "src" / "content" / "moments"

EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".heic", ".heif", ".tif", ".tiff"}
MAX_EDGE = 1400
QUALITY = 82


def convert(src: pathlib.Path, dst: pathlib.Path):
    img = Image.open(src)
    img = ImageOps.exif_transpose(img)
    if img.mode not in ("RGB",):
        img = img.convert("RGB")
    img.thumbnail((MAX_EDGE, MAX_EDGE), Image.LANCZOS)
    img.save(dst, "WEBP", quality=QUALITY, method=5)
    return img.size


def template(stamp: str, items):
    lines = [
        "---",
        f"date: {stamp}",
        "title: ",
        "text: ",
        "tags: []",
        "photos:",
    ]
    for it in items:
        lines.append(f"  - src: {it['src']}")
        lines.append(f"    w: {it['w']}")
        lines.append(f"    h: {it['h']}")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def append_to(path: pathlib.Path, items):
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    block = []
    for it in items:
        block.append(f"  - src: {it['src']}")
        block.append(f"    w: {it['w']}")
        block.append(f"    h: {it['h']}")

    for i, line in enumerate(lines):
        if line.strip() == "photos:":
            lines[i + 1 : i + 1] = block
            break
    else:
        marks = [i for i, l in enumerate(lines) if l.strip() == "---"]
        at = marks[1] if len(marks) > 1 else len(lines)
        lines[at:at] = ["photos:"] + block

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    if len(sys.argv) < 2:
        print("没有选文件夹")
        return 1

    folder = pathlib.Path(sys.argv[1])
    if not folder.is_dir():
        print("找不到这个文件夹：", folder)
        return 1

    files = [
        p for p in folder.iterdir()
        if p.is_file() and p.suffix.lower() in EXTS
    ]
    if not files:
        print("这个文件夹里没有照片。")
        return 1

    files.sort(key=lambda p: (p.stat().st_mtime, p.name))

    today = datetime.date.today()
    day = today.strftime("%Y-%m-%d")
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    outdir = OUT_ROOT / day
    outdir.mkdir(parents=True, exist_ok=True)

    start = 1
    existing = sorted(outdir.glob("*.webp"))
    if existing:
        try:
            start = max(int(p.stem) for p in existing) + 1
        except ValueError:
            start = len(existing) + 1

    items = []
    n = start
    ok = 0
    for src in files:
        name = f"{n:02d}.webp"
        dst = outdir / name
        try:
            w, h = convert(src, dst)
        except Exception as e:
            print(f"  跳过 {src.name}：{e}")
            continue
        size_kb = dst.stat().st_size // 1024
        print(f"  {name}  {w}×{h}  {size_kb} KB")
        items.append({"src": f"{day}/{name}", "w": w, "h": h})
        n += 1
        ok += 1

    if not ok:
        print("一张也没处理成功。")
        return 1

    md = CONTENT / f"{day}.md"
    if md.exists():
        append_to(md, items)
    else:
        md.write_text(template(stamp, items), encoding="utf-8")

    print()
    print(f"  存好 {ok} 张，写进了 src/content/moments/{day}.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())

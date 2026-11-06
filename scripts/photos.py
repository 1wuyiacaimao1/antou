"""把一个文件夹里的照片压成 webp，写进瞬间的内容文件。

用法：python scripts/photos.py "D:\某个文件夹"

已经导入过的照片会被跳过，靠文件内容的哈希记录，存在 photo-index.json 里。
"""
import datetime
import hashlib
import json
import pathlib
import sys
import traceback

from PIL import Image, ImageOps

try:
    import pillow_heif

    pillow_heif.register_heif_opener()
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT_ROOT = ROOT / "public" / "moments"
CONTENT = ROOT / "src" / "content" / "moments"
INDEX = ROOT / "photo-index.json"

EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".heic", ".heif", ".tif", ".tiff"}
MAX_EDGE = 1400
QUALITY = 82


def load_index():
    if INDEX.exists():
        try:
            return json.loads(INDEX.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_index(data):
    INDEX.write_text(
        json.dumps(data, ensure_ascii=False, indent=1, sort_keys=True),
        encoding="utf-8",
    )


def digest(path: pathlib.Path) -> str:
    h = hashlib.sha1()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def convert(src: pathlib.Path, dst: pathlib.Path):
    img = Image.open(src)
    img = ImageOps.exif_transpose(img)
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.thumbnail((MAX_EDGE, MAX_EDGE), Image.LANCZOS)
    img.save(dst, "WEBP", quality=QUALITY, method=5)
    return img.size


def template(stamp: str, items):
    lines = ["---", f"date: {stamp}", "title: ", "text: ", "tags: []", "photos:"]
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


def next_number(outdir: pathlib.Path) -> int:
    nums = []
    if outdir.exists():
        for p in outdir.glob("*.webp"):
            stem = p.stem.strip()
            if stem.isdigit():
                nums.append(int(stem))
    return (max(nums) + 1) if nums else 1


def run(folder_arg: str) -> int:
    folder = pathlib.Path(folder_arg)
    if not folder.is_dir():
        print("找不到这个文件夹：", folder)
        return 1

    files = [
        p
        for p in folder.iterdir()
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

    index = load_index()
    n = next_number(outdir)

    # 站里已经有的图，像素一样就不再重复导入
    out_hashes = set()
    for p in OUT_ROOT.rglob("*.webp"):
        try:
            out_hashes.add(digest(p))
        except Exception:
            pass

    items = []
    skipped = 0
    for src in files:
        try:
            h = digest(src)
        except Exception as e:
            print(f"  跳过 {src.name}：{e}")
            continue

        if h in index:
            skipped += 1
            continue

        name = f"{n:02d}.webp"
        dst = outdir / name
        try:
            w, hh = convert(src, dst)
        except Exception as e:
            print(f"  跳过 {src.name}：{e}")
            continue

        try:
            oh = digest(dst)
        except Exception:
            oh = ""
        if oh and oh in out_hashes:
            dst.unlink(missing_ok=True)
            skipped += 1
            continue
        if oh:
            out_hashes.add(oh)

        size_kb = dst.stat().st_size // 1024
        print(f"  {name}  {w}×{hh}  {size_kb} KB")
        items.append({"src": f"{day}/{name}", "w": w, "h": hh})
        index[h] = f"{day}/{name}"
        n += 1

    if skipped:
        print(f"  （{skipped} 张之前已经导入过，跳过）")

    if not items:
        print()
        print("  没有新照片，什么都没改。")
        return 0

    md = CONTENT / f"{day}.md"
    if md.exists():
        append_to(md, items)
    else:
        md.write_text(template(stamp, items), encoding="utf-8")

    save_index(index)

    print()
    print(f"  存好 {len(items)} 张，写进了 src/content/moments/{day}.md")
    return 0


def main():
    if len(sys.argv) < 2:
        print("没有选文件夹")
        return 1
    try:
        return run(sys.argv[1])
    except Exception:
        print()
        print("  出错了，把下面这段发给我：")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

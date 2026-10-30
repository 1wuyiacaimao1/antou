"""修复被写坏的 frontmatter。

有的编辑器打开文件时光标停在开头，人直接在 frontmatter 上面开始写，
结果开头变成「正文---」，frontmatter 被推到中间，构建就会报错。

做法：找到 date: 那一行，往回找最近的 --- 当开头，往后找下一行 --- 当结尾，
把整块搬到文件最前面，其余文字留在正文。
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).parent
CONTENT = ROOT / "src" / "content"

DATE_LINE = re.compile(r"^\s*date:\s*\S+", re.M)


def repair(path: pathlib.Path) -> bool:
    raw = path.read_text(encoding="utf-8")
    if raw.lstrip().startswith("---"):
        return False

    m = DATE_LINE.search(raw)
    if not m:
        return False

    # 往回找最近的 ---
    start = raw.rfind("---", 0, m.start())
    if start == -1:
        return False

    # 往后找下一行单独的 ---
    rest = raw[m.end():]
    close = re.search(r"\r?\n---[ \t]*\r?\n", rest)
    if not close:
        return False
    end = m.end() + close.end()

    block = raw[start:end]
    if not block.startswith("---"):
        return False
    block = block.replace("---", "---", 1)
    block = "---" + block[3:] if block[3:4] not in ("\r", "\n") else block
    block = "---\n" + block[3:].lstrip("\r\n")

    before = raw[:start].rstrip()
    after = raw[end:].lstrip("\r\n")

    body = (before + "\r\n\r\n" + after).strip("\r\n")
    fixed = block.rstrip("\r\n") + "\r\n\r\n" + body + "\r\n"
    path.write_text(fixed, encoding="utf-8")
    return True


def main():
    changed = 0
    for p in sorted(CONTENT.rglob("*.md")):
        if repair(p):
            print("修复了", p.relative_to(ROOT))
            changed += 1
    if changed == 0:
        print("没有需要修复的文件")


if __name__ == "__main__":
    main()

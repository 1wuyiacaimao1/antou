export interface ListItem {
  text: string;
  done: boolean;
  year: string;
}

/** 从正文里读出 `- [ ] 文字 @2026` 这样的行 */
export function parseItems(body: string): ListItem[] {
  const out: ListItem[] = [];
  for (const raw of body.split(/\r?\n/)) {
    const m = raw.match(/^\s*[-*]\s*\[([ xX])\]\s+(.+?)\s*$/);
    if (!m) continue;
    let text = m[2];
    let year = "";
    const y = text.match(/\s@(\d{4})$/);
    if (y) {
      year = y[1];
      text = text.slice(0, y.index).trim();
    }
    out.push({ text, done: m[1].toLowerCase() === "x", year });
  }
  return out;
}

export function countDone(items: ListItem[]) {
  return items.filter((i) => i.done).length;
}

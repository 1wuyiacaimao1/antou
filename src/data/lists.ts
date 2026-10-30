export interface ListItem {
  k: string;
  text: string;
  year?: string;
  done?: boolean;
}

export interface ListGroup {
  id: string;
  name: string;
  note: string;
  total: number;
  items: ListItem[];
}

export const lists: ListGroup[] = [
  {
    id: "films",
    name: "想看的电影",
    note: "最近加了三部老片，一直没找到时间",
    total: 23,
    items: [
      { k: "f1", text: "海边的曼彻斯特", year: "2025", done: true },
      { k: "f2", text: "花样年华", year: "2025", done: true },
      { k: "f3", text: "一一", year: "2025", done: true },
      { k: "f4", text: "雾中风景", year: "2025", done: true },
      { k: "f5", text: "四百击", year: "2025", done: true },
      { k: "f6", text: "樱桃的滋味" },
      { k: "f7", text: "东京物语", year: "2024", done: true },
      { k: "f8", text: "春夏秋冬又一春" },
      { k: "f9", text: "帕特森" },
      { k: "f10", text: "郊游", year: "2024", done: true },
    ],
  },
  {
    id: "weekends",
    name: "想去的周末",
    note: "都在两小时车程以内",
    total: 9,
    items: [
      { k: "w1", text: "四明山", year: "2026", done: true },
      { k: "w2", text: "象山海边", year: "2026", done: true },
      { k: "w3", text: "天台山" },
      { k: "w4", text: "前童古镇" },
    ],
  },
  {
    id: "try",
    name: "待尝试",
    note: "做饭、修东西、和一些说不上来的事",
    total: 12,
    items: [
      { k: "t1", text: "自己煮一次红烧肉", year: "2026", done: true },
      { k: "t2", text: "把台灯拆开修一下", year: "2026", done: true },
      { k: "t3", text: "用木头做个小盒子" },
      { k: "t4", text: "学一次水彩" },
    ],
  },
  {
    id: "books",
    name: "要读的书",
    note: "教科书不算在内",
    total: 18,
    items: [
      { k: "b1", text: "《城与不确定的墙》", year: "2026", done: true },
      { k: "b2", text: "《小说机杼》" },
      { k: "b3", text: "《我们仨》" },
    ],
  },
];

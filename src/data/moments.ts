export interface Moment {
  d: string;
  title: string;
  text: string;
  tags: string;
  colors: [string, string];
  w: number;
  h: number;
}

export const moments: Moment[] = [
  {
    d: "10.14 星期三",
    title: "东钱湖",
    text: "风把水面吹出一层细纹，站了很久。回来的时候下坡，一路没踩踏板。",
    tags: "湖边 · 出门",
    colors: ["#E6DCC8", "#D3C5AB"],
    w: 540,
    h: 352,
  },
  {
    d: "10.08 星期四",
    title: "宿舍窗台",
    text: "下午四点的光刚好落在桌角，把水杯的影子拉得很长。",
    tags: "光 · 日常",
    colors: ["#EDE4D4", "#DDD2BC"],
    w: 282,
    h: 352,
  },
  {
    d: "10.02 星期日",
    title: "雨后的操场",
    text: "一个人也没有。跑道边缘还积着水，映着灰白的天。",
    tags: "雨 · 学校",
    colors: ["#E3DDCE", "#CFC7B4"],
    w: 540,
    h: 352,
  },
  {
    d: "09.26 星期六",
    title: "食堂的窗",
    text: "玻璃上起了雾，随手画了个圈，外面的人从圈里走过去。",
    tags: "雾 · 食堂",
    colors: ["#E9E2D1", "#DCD3BE"],
    w: 352,
    h: 352,
  },
  {
    d: "09.20 星期日",
    title: "图书馆四楼",
    text: "靠窗那张桌子空着，坐下来之后发现暖气很足。",
    tags: "图书馆",
    colors: ["#E7DFCE", "#D5C9B1"],
    w: 540,
    h: 352,
  },
];

export interface Bookmark {
  mark: string;
  name: string;
  why: string;
  host: string;
  href: string;
}

export interface BookmarkGroup {
  name: string;
  links: Bookmark[];
}

export const groups: BookmarkGroup[] = [
  {
    name: "常 用 工 具",
    links: [
      { mark: "G", name: "GitHub", why: "代码和这个网站本身都在这", host: "github.com", href: "https://github.com" },
      { mark: "O", name: "Overleaf", why: "写公式作业比 Word 快，模板存了两套", host: "overleaf.com", href: "https://www.overleaf.com" },
      { mark: "D", name: "DeepL", why: "英文教材的段落过一遍，比逐句查快", host: "deepl.com", href: "https://www.deepl.com" },
    ],
  },
  {
    name: "学 习",
    links: [
      { mark: "L", name: "LeetCode", why: "每天一两道，连续记在清单里", host: "leetcode.cn", href: "https://leetcode.cn" },
      { mark: "洛", name: "洛谷", why: "题单比力扣更适合打基础", host: "luogu.com.cn", href: "https://www.luogu.com.cn" },
      { mark: "A", name: "arXiv", why: "看摘要就够，正文留给以后", host: "arxiv.org", href: "https://arxiv.org" },
      { mark: "M", name: "MDN", why: "前端的东西只信这个", host: "developer.mozilla.org", href: "https://developer.mozilla.org" },
    ],
  },
  {
    name: "文 章",
    links: [
      { mark: "少", name: "少数派", why: "偶尔有讲工作流的好文章", host: "sspai.com", href: "https://sspai.com" },
      { mark: "阮", name: "阮一峰的网络日志", why: "每周五那篇，看完能跟上一点", host: "ruanyifeng.com", href: "https://www.ruanyifeng.com" },
    ],
  },
  {
    name: "别 人 的 站",
    links: [
      { mark: "K", name: "Kagi Small Web", why: "随机跳到一个陌生人的小站，比刷推荐有意思", host: "kagi.com", href: "https://kagi.com" },
      { mark: "N", name: "Neal.fun", why: "无聊的时候点开，能待很久", host: "neal.fun", href: "https://neal.fun" },
    ],
  },
];

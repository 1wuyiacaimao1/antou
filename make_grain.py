"""生成深胡桃木木纹 SVG，并内联成 data URI 注入页面。
纹理走向用贝塞尔曲线做轻微弯曲和宽窄变化，带少量短分叉，不出现整齐平行直线。
"""
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
W, H = 1400, 700


def build_svg(seed: int = 20261020) -> str:
    rnd = random.Random(seed)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" preserveAspectRatio="none">',
        '<g fill="none" stroke-linecap="round">',
    ]

    y = -20
    while y < H + 20:
        # 每条纹理的基线与参数都不同
        amp = rnd.uniform(5, 16)
        thick = rnd.uniform(0.8, 2.8)
        light = rnd.random() < 0.45
        color = "rgb(214,186,150)" if light else "rgb(16,10,6)"
        op = rnd.uniform(0.020, 0.055) if light else rnd.uniform(0.075, 0.16)

        # 分段画，避免一根线从头贯到尾
        x = -60
        while x < W + 60:
            seg = rnd.uniform(220, 520)
            x2 = x + seg
            c1 = (x + seg * 0.32, y + rnd.uniform(-amp, amp))
            c2 = (x + seg * 0.68, y + rnd.uniform(-amp, amp))
            end_y = y + rnd.uniform(-amp * 0.5, amp * 0.5)
            d = (f"M{x:.1f} {y + rnd.uniform(-1.2, 1.2):.1f} "
                 f"C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {x2:.1f} {end_y:.1f}")
            parts.append(f'<path d="{d}" stroke="{color}" stroke-opacity="{op:.3f}" '
                         f'stroke-width="{thick * rnd.uniform(0.7, 1.3):.2f}"/>')

            # 少量自然分叉：从这条线上斜着岔出去一小段
            if rnd.random() < 0.22:
                sx = x + seg * rnd.uniform(0.2, 0.8)
                sy = y + rnd.uniform(-amp * 0.4, amp * 0.4)
                ex, ey = sx + rnd.uniform(-90, 90), sy + rnd.uniform(8, 26)
                parts.append(
                    f'<path d="M{sx:.1f} {sy:.1f} Q{(sx+ex)/2:.1f} {(sy+ey)/2 + rnd.uniform(-4,4):.1f} '
                    f'{ex:.1f} {ey:.1f}" stroke="{color}" stroke-opacity="{op*0.7:.3f}" '
                    f'stroke-width="{thick*0.6:.2f}"/>'
                )
            x = x2
        y += rnd.uniform(14, 34)

    parts.append("</g></svg>")
    return "".join(parts)


def to_data_uri(svg: str) -> str:
    svg = svg.replace('"', "'")
    svg = svg.replace("<", "%3C").replace(">", "%3E").replace("#", "%23")
    svg = re.sub(r"\s+", " ", svg).strip()
    return "data:image/svg+xml," + svg


if __name__ == "__main__":
    svg = build_svg()
    uri = to_data_uri(svg)
    print(f"svg {len(svg)/1024:.1f} KB, data uri {len(uri)/1024:.1f} KB")
    (ROOT / "wood-grain.svg").write_text(svg, encoding="utf-8")

    target = ROOT / (sys.argv[1] if len(sys.argv) > 1 else "home.html")
    if target.exists():
        html = target.read_text(encoding="utf-8")
        if "%%GRAIN%%" in html:
            html = html.replace("%%GRAIN%%", uri)
            target.write_text(html, encoding="utf-8")
            print(f"已注入 {target.name}")

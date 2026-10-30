"""把首页装饰往“手画”拉一点：加一层极轻的位移噪声，并把盆栽、转椅的规整结构打散。"""
import pathlib
import re

P = pathlib.Path(r"D:\hanacoagent\life-site\home.html")
s = P.read_text(encoding="utf-8")
report = []

# 1) 插入噪声滤镜定义
if 'id="wobble"' not in s:
    s = s.replace(
        "<body>",
        "<body>\n\n"
        '<svg width="0" height="0" style="position:absolute" aria-hidden="true">\n'
        "  <defs>\n"
        '    <filter id="wobble" x="-10%" y="-10%" width="120%" height="120%">\n'
        "      <feTurbulence type=\"fractalNoise\" baseFrequency=\"0.055\" numOctaves=\"2\" seed=\"11\" result=\"n\"/>\n"
        "      <feDisplacementMap in=\"SourceGraphic\" in2=\"n\" scale=\"1.6\"\n"
        "        xChannelSelector=\"R\" yChannelSelector=\"G\"/>\n"
        "    </filter>\n"
        "  </defs>\n"
        "</svg>\n",
        1,
    )
    report.append("filter inserted")

# 2) 把噪声挂到所有装饰上（CSS 过滤器链，一次改两处）
s2 = s.replace(
    "  .deco{position:absolute;pointer-events:none;\n        filter:drop-shadow(4px 9px 11px rgba(20,12,6,.45))}",
    "  .deco{position:absolute;pointer-events:none;\n        filter:url(#wobble) drop-shadow(4px 9px 11px rgba(20,12,6,.45))}",
    1,
)
if s2 != s:
    report.append("deco filter")
s = s2

s2 = s.replace(
    "  .floor-obj{position:absolute;pointer-events:none;\n             filter:drop-shadow(6px 12px 14px rgba(60,45,30,.18))}",
    "  .floor-obj{position:absolute;pointer-events:none;\n             filter:url(#wobble) drop-shadow(6px 12px 14px rgba(60,45,30,.18))}",
    1,
)
if s2 != s:
    report.append("floor filter")
s = s2

# 3) 盆栽：盆口改成略椭，叶子角度打散
old_pot = (
    '      <circle cx="55" cy="55" r="46" fill="var(--pot)"/>\n'
    '      <circle cx="55" cy="55" r="38" fill="#A08D74"/>'
)
new_pot = (
    '      <ellipse cx="55" cy="55.6" rx="46.6" ry="45" fill="var(--pot)"/>\n'
    '      <ellipse cx="55" cy="56" rx="38.3" ry="37.2" fill="#A08D74"/>'
)
if old_pot in s:
    s = s.replace(old_pot, new_pot, 1)
    report.append("pot ellipse")

old_out = (
    '      <circle cx="55" cy="55" r="46" class="out"/>\n'
    '      <circle cx="55" cy="55" r="38" class="out" opacity=".5"/>'
)
new_out = (
    '      <ellipse cx="55" cy="55.6" rx="46.6" ry="45" class="out"/>\n'
    '      <ellipse cx="55" cy="56" rx="38.3" ry="37.2" class="out" opacity=".5"/>'
)
if old_out in s:
    s = s.replace(old_out, new_out, 1)
    report.append("pot outline")

old_center = '      <circle cx="55" cy="55" r="6" fill="#8C7A60"/>'
new_center = '      <ellipse cx="55.4" cy="55.2" rx="6.2" ry="5.7" fill="#8C7A60"/>'
if old_center in s:
    s = s.replace(old_center, new_center, 1)
    report.append("soil center")

# 叶子：角度 5 / 64 / 119 / 173 / 237 / 299，尺寸各异
leaf_start = s.find("        <ellipse cx=\"55\" cy=\"30\" rx=\"13\" ry=\"6.5\" fill=\"var(--leaf)\"/>")
if leaf_start != -1:
    leaf_end = s.find("      </g>", leaf_start)
    new_leaves = (
        '        <ellipse cx="54.5" cy="28.5" rx="13.6" ry="6.3" transform="rotate(5 54.5 28.5)" fill="var(--leaf)"/>\n'
        '        <ellipse cx="54.5" cy="28.5" rx="13.6" ry="6.3" transform="rotate(5 54.5 28.5)" class="out"/>\n'
        '        <ellipse cx="77.6" cy="40" rx="12.1" ry="6.9" transform="rotate(64 77.6 40)" fill="var(--leaf-2)"/>\n'
        '        <ellipse cx="77.6" cy="40" rx="12.1" ry="6.9" transform="rotate(64 77.6 40)" class="out"/>\n'
        '        <ellipse cx="79.4" cy="66.6" rx="13.4" ry="5.9" transform="rotate(119 79.4 66.6)" fill="var(--leaf)"/>\n'
        '        <ellipse cx="79.4" cy="66.6" rx="13.4" ry="5.9" transform="rotate(119 79.4 66.6)" class="out"/>\n'
        '        <ellipse cx="55.6" cy="81.6" rx="11.1" ry="5.5" transform="rotate(173 55.6 81.6)" fill="var(--leaf-2)"/>\n'
        '        <ellipse cx="55.6" cy="81.6" rx="11.1" ry="5.5" transform="rotate(173 55.6 81.6)" class="out"/>\n'
        '        <ellipse cx="30.8" cy="70.2" rx="13.5" ry="6.7" transform="rotate(237 30.8 70.2)" fill="var(--leaf)"/>\n'
        '        <ellipse cx="30.8" cy="70.2" rx="13.5" ry="6.7" transform="rotate(237 30.8 70.2)" class="out"/>\n'
        '        <ellipse cx="29.4" cy="40.8" rx="12" ry="6.1" transform="rotate(299 29.4 40.8)" fill="var(--leaf-2)"/>\n'
        '        <ellipse cx="29.4" cy="40.8" rx="12" ry="6.1" transform="rotate(299 29.4 40.8)" class="out"/>\n'
    )
    s = s[:leaf_start] + new_leaves + s[leaf_end:]
    report.append("leaves scattered")

# 4) 转椅：五条腿不再精确 72 度
old_arms = (
    '          <use href="#arm"/>\n'
    '          <use href="#arm" transform="rotate(72)"/>\n'
    '          <use href="#arm" transform="rotate(144)"/>\n'
    '          <use href="#arm" transform="rotate(216)"/>\n'
    '          <use href="#arm" transform="rotate(288)"/>'
)
new_arms = (
    '          <use href="#arm" transform="rotate(0) scale(1.01)"/>\n'
    '          <use href="#arm" transform="rotate(71) scale(0.985)"/>\n'
    '          <use href="#arm" transform="rotate(146) scale(1.015)"/>\n'
    '          <use href="#arm" transform="rotate(217) scale(0.99)"/>\n'
    '          <use href="#arm" transform="rotate(290) scale(1.005)"/>'
)
if old_arms in s:
    s = s.replace(old_arms, new_arms, 1)
    report.append("chair arms jittered")

# 5) 水杯：水面偏一点
old_glass = (
    '      <circle cx="40" cy="40" r="27" fill="var(--glass-fill)"/>\n'
    '      <circle cx="40" cy="40" r="23" fill="var(--water)"/>'
)
new_glass = (
    '      <circle cx="40.4" cy="39.6" r="27" fill="var(--glass-fill)"/>\n'
    '      <circle cx="39.7" cy="40.6" r="22.7" fill="var(--water)"/>'
)
if old_glass in s:
    s = s.replace(old_glass, new_glass, 1)
    report.append("glass offset")

P.write_text(s, encoding="utf-8")
print(" | ".join(report) if report else "no change")

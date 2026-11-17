import re, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# (file, label, colour on navy, motion)
icons = [
    ('kotlin', 'Kotlin', '7F52FF', 'flip'),
    ('android', 'Android', '3DDC84', 'bob'),
    ('androidstudio', 'Studio', '3DDC84', 'tilt'),
    ('jetpackcompose', 'Compose', '4285F4', 'spin'),
    ('materialdesign', 'Material', 'E3E3E3', 'breathe'),
    ('gradle', 'Gradle', '7FD3E0', 'hop'),
    ('ktor', 'Ktor', '3E9BFF', 'dash'),
    ('sqlite', 'SQLite', '5AB4E6', 'sway'),
    ('firebase', 'Firebase', 'FF7A2E', 'flicker'),
    ('googlecloud', 'Cloud', '4285F4', 'drift'),
    ('googlegemini', 'Gemini', 'A58BE0', 'twinkle'),
    ('claude', 'Claude', 'D97757', 'burst'),
    ('onnx', 'ONNX', '4D8CFF', 'turn'),
    ('typescript', 'TypeScript', '3178C6', 'type'),
    ('nodedotjs', 'Node.js', '5FA04E', 'hex'),
    ('figma', 'Figma', 'F24E1E', 'pop'),
    ('postman', 'Postman', 'FF6C37', 'launch'),
    ('git', 'Git', 'F05032', 'swing'),
    ('github', 'GitHub', 'FFFFFF', 'wiggle'),
    ('googleplay', 'Play', '3DDC84', 'play'),
]

T, G, PER_ROW = 76, 18, 10
ROW_H = T + 46
W = PER_ROW * T + (PER_ROW - 1) * G + 8
H = 2 * ROW_H + 24

tiles = ''
for k, (f, label, col, motion) in enumerate(icons):
    path = re.search(r'<path d="([^"]+)"', open(f'si/{f}.svg', encoding='utf-8').read()).group(1)
    row, colm = divmod(k, PER_ROW)
    x = 4 + colm * (T + G)
    y = 14 + row * ROW_H
    d = k * 0.12
    tiles += f'''  <g class="tile" style="animation-delay:{k * 0.06:.2f}s, {1 + d:.2f}s">
    <rect class="halo" style="animation-delay:{1 + d:.2f}s" x="{x - 3}" y="{y - 3}" width="{T + 6}" height="{T + 6}" rx="10" fill="none" stroke="#{col}" stroke-width="2"/>
    <rect x="{x}" y="{y}" width="{T}" height="{T}" rx="8" fill="#18304D" stroke="#F5C842" stroke-opacity=".18"/>
    <g transform="translate({x + T / 2 - 18} {y + T / 2 - 18}) scale(1.5)"><path d="{path}" fill="#{col}"/></g>
    <text x="{x + T / 2}" y="{y + T + 22}" text-anchor="middle" class="lbl">{label}</text>
  </g>
'''

css = """
    .lbl { font: 600 13px 'Segoe UI', -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif; fill: #9FB4CC; }
    /* Pop in one by one, then ride a wave across the rows */
    .tile { opacity: 0; transform-box: fill-box; transform-origin: center;
            animation: in .6s cubic-bezier(.3,1.6,.5,1) forwards, wave 3.6s ease-in-out infinite; }
    @keyframes in { from { opacity: 0; transform: translateY(14px) scale(.6); } to { opacity: 1; transform: none; } }
    @keyframes wave { 0%, 30%, 100% { opacity: 1; transform: translateY(0); } 12% { opacity: 1; transform: translateY(-10px); } }
    /* A ring in the brand colour glows as each tile lifts */
    .halo { opacity: 0; animation: halo 3.6s ease-in-out infinite; }
    @keyframes halo { 0%, 30%, 100% { opacity: 0; } 12% { opacity: .9; } }
    @media (prefers-reduced-motion: reduce) { .tile, .halo { animation: none !important; } .tile { opacity: 1; } }
"""

names = ', '.join(i[1] for i in icons)
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{names}">
  <style>{css}  </style>
{tiles}</svg>
'''
open('../assets/tech-stack-v3.svg', 'w', encoding='utf-8', newline='\n').write(svg)
print(W, H, len(icons))

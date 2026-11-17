import os, base64
os.chdir(os.path.dirname(os.path.abspath(__file__)))
FONT64 = base64.b64encode(open('font/outfit-stats.woff2', 'rb').read()).decode()

CW, CH, GAP = 222, 150, 14
W = 4 * CW + 3 * GAP + 4
TOP = GAP - 2  # the card outline already sits 2 units down
H = CH + 4 + TOP

# (count-up frames, label, icon builder)
def icon_downloads(cx, cy):
    return f'''<g class="dl">
      <path d="M{cx-14} {cy+6} v8 h28 v-8" fill="none" stroke="#9CC0E8" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>
      <g class="dl-arrow"><path d="M{cx} {cy-16} v18 M{cx-7} {cy-4} l7 7 l7 -7" fill="none" stroke="#3DDC84" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/></g>
    </g>'''

def icon_star(cx, cy):
    pts = []
    import math
    for i in range(10):
        r = 15 if i % 2 == 0 else 6.5
        a = -math.pi / 2 + i * math.pi / 5
        pts.append(f'{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}')
    return f'''<g class="star"><polygon points="{' '.join(pts)}" fill="#F5C842"/></g>
    <g class="spark s1"><path d="M{cx+19} {cy-15} v8 M{cx+15} {cy-11} h8" stroke="#FFE7A3" stroke-width="2" stroke-linecap="round"/></g>
    <g class="spark s2"><path d="M{cx-20} {cy+6} v6 M{cx-23} {cy+9} h6" stroke="#FFE7A3" stroke-width="2" stroke-linecap="round"/></g>'''

def icon_ads(cx, cy):
    return f'''<rect x="{cx-17}" y="{cy-11}" width="34" height="22" rx="4" fill="none" stroke="#9CC0E8" stroke-width="3"/>
    <text x="{cx}" y="{cy+5}" text-anchor="middle" class="adtxt">ADS</text>
    <path class="strike" d="M{cx-21} {cy+14} L{cx+21} {cy-14}" stroke="#FF4A3D" stroke-width="4" stroke-linecap="round"/>'''

def icon_apps(cx, cy):
    out = ''
    cols = ['#7F52FF', '#3DDC84', '#4285F4', '#F5C842', '#FF7A2E', '#D97757', '#A58BE0', '#5AB4E6', '#F05032']
    for i in range(9):
        r, c = divmod(i, 3)
        out += f'<rect class="app" style="animation-delay:{i * .12:.2f}s" x="{cx - 15 + c * 11}" y="{cy - 15 + r * 11}" width="8" height="8" rx="2" fill="{cols[i]}"/>'
    return out

stats = [
    (['0', '900', '2,100', '3,600', '5,000', '6,000'], '6,500+', 'downloads across apps', icon_downloads),
    (['0', '20', '50', '80', '110', '135'], '150+', 'ratings across apps', icon_star),
    (['5', '4', '3', '2', '1'], '0', 'ads in any app', icon_ads),
    (['1', '3', '5', '7', '8'], '9', 'apps built from scratch', icon_apps),
]

STEP = .11
cards = ''
for k, (frames, final, label, icon) in enumerate(stats):
    x = 2 + k * (CW + GAP)
    cx = x + CW / 2
    start = .3 + k * .15
    nums = f'<text class="num" x="{cx}" y="104">{final}</text>'
    cards += f'''  <g class="card">
    <rect x="{x}" y="2" width="{CW}" height="{CH}" rx="4" fill="#18304D" stroke="#F5C842" stroke-opacity=".22"/>
    <rect x="{x}" y="2" width="{CW}" height="3" fill="#F5C842" fill-opacity=".85"/>
    {icon(cx, 44)}
    {nums}
    <text class="lbl" x="{cx}" y="132">{label}</text>
  </g>
'''

css = """
    @font-face { font-family: 'Outfit'; font-weight: 100 900; src: url(data:font/woff2;base64,FONT64) format('woff2'); }
    .num { font: 700 34px 'Outfit', 'Segoe UI', -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif; fill: #FFF8E7; text-anchor: middle; }
    .lbl { font: 500 13.5px 'Outfit', 'Segoe UI', -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif; fill: #9FB4CC; text-anchor: middle; }
    .adtxt { font: 800 11px 'Outfit', 'Segoe UI', -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif; fill: #9CC0E8; letter-spacing: .5px; }



    /* Downloads: the arrow keeps dropping into the tray */
    .dl-arrow { animation: drop 1.8s ease-in-out infinite; }
    @keyframes drop { 0% { transform: translateY(-6px); opacity: 0; } 30% { opacity: 1; } 60% { transform: translateY(3px); opacity: 1; } 100% { transform: translateY(3px); opacity: 0; } }

    /* Rating: the star turns and twinkles */
    .star { transform-box: fill-box; transform-origin: center; animation: twirl 3.2s ease-in-out infinite; }
    @keyframes twirl { 0%, 70%, 100% { transform: rotate(0) scale(1); } 80% { transform: rotate(72deg) scale(1.2); } 90% { transform: rotate(72deg) scale(.95); } }
    .spark { opacity: 0; animation: spark 3.2s ease-in-out infinite; }
    .s2 { animation-delay: .25s; }
    @keyframes spark { 0%, 72%, 100% { opacity: 0; } 82% { opacity: 1; } }

    /* No ads: the strike keeps slashing through */
    .strike { stroke-dasharray: 60; animation: slash 2.6s ease-in-out infinite; }
    @keyframes slash { 0%, 15% { stroke-dashoffset: 60; } 35%, 85% { stroke-dashoffset: 0; } 100% { stroke-dashoffset: -60; } }

    /* Nine apps: tiles pop in one by one */
    .app { transform-box: fill-box; transform-origin: center; animation: app 3s cubic-bezier(.3,1.6,.5,1) infinite; }
    @keyframes app { 0% { transform: scale(0); } 12%, 80% { transform: scale(1); } 92%, 100% { transform: scale(0); } }

    @media (prefers-reduced-motion: reduce) {
      * { animation: none !important; }
    }
"""

css = css.replace('FONT64', FONT64)
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="6,500+ downloads across apps; 150+ ratings across apps; 0 ads in any app; 9 apps built from scratch">
  <style>{css}  </style>
<g transform="translate(0 {TOP})">
{cards}</g>
</svg>
'''
open('../assets/stats.svg', 'w', encoding='utf-8', newline='\n').write(svg)
print(W, H)

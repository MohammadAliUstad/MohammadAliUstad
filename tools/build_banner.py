import base64, random, math, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
random.seed(7)
font64 = base64.b64encode(open('font/outfit-sub.woff2', 'rb').read()).decode()
rgb = base64.b64encode(open('fig_rgb.jpg', 'rb').read()).decode()
msk = base64.b64encode(open('fig_mask.jpg', 'rb').read()).decode()


def bolt(x1, y1, x2, y2, disp, depth=5):
    pts = [(x1, y1), (x2, y2)]
    for _ in range(depth):
        new = [pts[0]]
        for (ax, ay), (bx, by) in zip(pts, pts[1:]):
            mx, my = (ax + bx) / 2, (ay + by) / 2
            dx, dy = bx - ax, by - ay
            L = math.hypot(dx, dy) or 1
            o = random.uniform(-disp, disp)
            new += [(mx - dy / L * o, my + dx / L * o), (bx, by)]
        pts = new
        disp *= 0.55
    return pts


def d(pts):
    return 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts)


def boltgroup(x1, y1, x2, y2, disp):
    main = bolt(x1, y1, x2, y2, disp)
    paths = [(d(main), 1.0)]
    for _ in range(random.randint(1, 3)):
        i = random.randint(len(main) // 5, len(main) * 3 // 4)
        sx, sy = main[i]
        ang = math.atan2(y2 - y1, x2 - x1) + random.choice([-1, 1]) * random.uniform(.4, .9)
        L = math.hypot(x2 - x1, y2 - y1) * random.uniform(.25, .45)
        paths.append((d(bolt(sx, sy, sx + math.cos(ang) * L, sy + math.sin(ang) * L, disp * .5, 4)), 0.6))
    return paths


# Bolts start on Sanji's outline (traced from the mask) and shoot outward
CX, CY = 215, 215


from PIL import Image
_m = Image.open('fig_mask.jpg').convert('L').resize((420, 420)).load()


def near_body(x, y, gap=14):
    for ox in range(-gap, gap + 1, 2):
        for oy in range(-gap, gap + 1, 2):
            px, py = int(x + ox), int(y + oy)
            if 0 <= px < 420 and 0 <= py < 420 and _m[px, py] > 128:
                return True
    return False


def from_body(x, y, deg, length, layer, inset=8):
    """Grows out of Sanji's outline; the outer end is free."""
    a = math.radians(deg)
    ux, uy = (x - CX), (y - CY)
    n = math.hypot(ux, uy) or 1
    sx, sy = x - ux / n * inset, y - uy / n * inset
    return ((sx, sy), (sx + math.cos(a) * length, sy + math.sin(a) * length), length * .22, layer)


def from_edge(x, y, ex, ey, layer='back'):
    """Reaches in from a banner edge and stops short of Sanji."""
    # pull the free end back until it's clear of his outline
    for _ in range(60):
        if not near_body(ex, ey):
            break
        ex, ey = x + (ex - x) * .9, y + (ey - y) * .9
    L = math.hypot(ex - x, ey - y)
    return ((x, y), (ex, ey), L * .22, layer)


specs = [
    from_body(116, 188, -170, 140, 'back'),   # left of the face
    from_body(105, 105, -140, 150, 'back'),   # hair, upper left
    from_body(172, 53, -110, 110, 'back'),    # top of the hair
    from_body(254, 71, -65, 130, 'back'),     # hair, upper right
    from_body(313, 117, -40, 170, 'back'),    # right of the head
    from_body(322, 186, -10, 160, 'back'),    # right cheek
    from_body(30, 300, -120, 150, 'back'),    # left shoulder
    from_body(82, 138, -155, 120, 'front'),   # hair tip, left
    from_body(215, 52, -88, 70, 'front'),     # crown
    from_body(326, 152, -25, 150, 'front'),   # right side of the head
    from_body(355, 330, -20, 105, 'front'),   # right shoulder
]
groups = {'back': '', 'front': ''}
for (x1, y1), (x2, y2), disp, layer in specs:
    dur = random.choice([2.6, 3.1, 3.7, 4.3])
    delay = -random.uniform(0, dur)
    body = ''
    for pd, w in boltgroup(x1, y1, x2, y2, disp):
        body += (f'<path d="{pd}" class="halo" stroke-width="{16 * w:.1f}"/>'
                 f'<path d="{pd}" class="dark" stroke-width="{9 * w:.1f}"/>'
                 f'<path d="{pd}" class="core" stroke-width="{5 * w:.1f}"/>'
                 f'<path d="{pd}" class="hot" stroke-width="{1.6 * w:.1f}"/>')
    groups[layer] += f'    <g class="bolt" style="animation-duration:{dur}s;animation-delay:{delay:.2f}s">{body}</g>\n'

tx, ty = 903, 267


puffs = ''
N = 24
for i in range(N):
    dur = 16.0
    delay = -dur * i / N
    variant = i % 3 + 1
    r = random.uniform(20, 30)
    sx = random.uniform(10, 420)
    sy = random.uniform(330, 440)
    puffs += (f'      <circle class="puff p{variant}" cx="{sx:.0f}" cy="{sy:.0f}" r="{r:.1f}" '
              f'style="animation-delay:{delay:.2f}s"/>\n')
smoke = f"""    <g class="smoke" filter="url(#smokefx)">
{puffs}    </g>
"""

CSS = """
      @font-face { font-family: 'Outfit'; font-weight: 100 900; src: url(data:font/woff2;base64,FONT64) format('woff2'); }
      .font { font-family: 'Outfit', 'Segoe UI', -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif; }

      /* Smoke billowing up from behind him */
      .puff { fill: #F5F5F5; opacity: 0; transform-box: fill-box; transform-origin: center;
              animation: 16s cubic-bezier(.35,.1,.45,1) infinite; }
      .p1 { animation-name: drift1; } .p2 { animation-name: drift2; } .p3 { animation-name: drift3; }
      @keyframes drift1 {
        0%   { opacity: 0;   transform: translate(0, 0) scale(.9); }
        18%  { opacity: .2; }
        55%  { opacity: .16; transform: translate(-18px, -190px) scale(2.6); }
        85%  { opacity: .07; transform: translate(-30px, -320px) scale(3.8); }
        100% { opacity: 0;   transform: translate(-38px, -400px) scale(4.5); }
      }
      @keyframes drift2 {
        0%   { opacity: 0;   transform: translate(0, 0) scale(.9); }
        18%  { opacity: .2; }
        55%  { opacity: .16; transform: translate(12px, -190px) scale(2.6); }
        85%  { opacity: .07; transform: translate(22px, -320px) scale(3.8); }
        100% { opacity: 0;   transform: translate(28px, -400px) scale(4.5); }
      }
      @keyframes drift3 {
        0%   { opacity: 0;   transform: translate(0, 0) scale(.9); }
        18%  { opacity: .2; }
        55%  { opacity: .16; transform: translate(-4px, -190px) scale(2.6); }
        85%  { opacity: .07; transform: translate(-10px, -320px) scale(3.8); }
        100% { opacity: 0;   transform: translate(4px, -400px) scale(4.5); }
      }

      /* Red and black lightning crackling around him */
      .bolt path { fill: none; stroke-linecap: round; stroke-linejoin: round; }
      .bolt .halo { stroke: #FF2020; filter: url(#glow); opacity: .9; }
      .bolt .dark { stroke: #000000; }
      .bolt .core { stroke: #FF2A1F; }
      .bolt .hot { stroke: #FF9C8A; }
      .bolt { opacity: BOLT_OPACITY; animation: crack 3s steps(1, end) infinite; }
      @keyframes crack {
        0%   { opacity: 1; }
        3%   { opacity: 0; }
        5%   { opacity: 1; }
        9%   { opacity: .5; }
        12%  { opacity: 1; }
        16%  { opacity: 0; }
        100% { opacity: 0; }
      }
      .aura { animation: surge 3s ease-in-out infinite; transform-origin: 215px 190px; }
      @keyframes surge { 0%,100% { opacity: .55; transform: scale(1); } 50% { opacity: 1; transform: scale(1.08); } }

      @media (prefers-reduced-motion: reduce) {
        .puff, .bolt, .aura { animation: none; }
      }
"""


def build(preview=False):
    css = CSS.replace('BOLT_OPACITY', '0').replace('FONT64', font64)
    if preview:
        css = css.replace('animation: crack 3s', 'opacity: 1; animation-name: none; animation-duration: 3s')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1280" height="420" viewBox="0 0 1280 420" role="img" aria-label="Mohammad Ali · Android Developer · Founder, Yugen Tech">
  <defs>
    <filter id="smokefx" x="-60%" y="-60%" width="220%" height="220%">
      <feTurbulence type="fractalNoise" baseFrequency="0.012 0.02" numOctaves="4" seed="4" result="noise">
        <animate attributeName="baseFrequency" dur="30s" values="0.012 0.02;0.015 0.024;0.012 0.02" repeatCount="indefinite"/>
      </feTurbulence>
      <feGaussianBlur in="SourceGraphic" stdDeviation="11" result="blur"/>
      <feDisplacementMap in="blur" in2="noise" scale="60" xChannelSelector="R" yChannelSelector="G"/>
    </filter>
    <filter id="glow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="5"/></filter>
    <radialGradient id="aura" cx="0.5" cy="0.45" r="0.5">
      <stop offset="0" stop-color="#FF1E1E" stop-opacity=".55"/>
      <stop offset=".55" stop-color="#B00000" stop-opacity=".22"/>
      <stop offset="1" stop-color="#B00000" stop-opacity="0"/>
    </radialGradient>
    <mask id="cut" maskUnits="userSpaceOnUse" x="0" y="0" width="420" height="420">
      <image x="0" y="0" width="420" height="420" href="data:image/jpeg;base64,{msk}"/>
    </mask>
    <clipPath id="card"><rect width="1280" height="420" rx="4"/></clipPath>
    <style>{css}    </style>
  </defs>

  <g clip-path="url(#card)">
    <rect width="1280" height="420" fill="#18304D"/>

    <!-- Lightning behind him -->
{groups['back']}
    <!-- The supplied artwork, cut out with its own mask -->
    <image x="0" y="0" width="420" height="420" mask="url(#cut)" href="data:image/jpeg;base64,{rgb}"/>

    <!-- Lightning crossing in front -->
{groups['front']}  </g>
  <rect x="0.5" y="0.5" width="1279" height="419" rx="4" fill="none" stroke="#F5C842" stroke-opacity="0.18"/>

  <g class="font" text-anchor="middle">
    <text x="850" y="118" fill="#F5C842" font-size="24" font-weight="600" letter-spacing="0.5">Android Developer · Founder, Yugen Tech</text>
    <text x="850" y="212" fill="#FFF8E7" font-size="84" font-weight="700" letter-spacing="-1">Mohammad Ali</text>
    <text x="850" y="262" fill="#D6E2F0" font-size="21" font-weight="400" fill-opacity="0.9">Calm, crafted apps that people actually use. No ads, no compromises.</text>
  </g>

  <g class="font" font-size="17" font-weight="600" text-anchor="middle">
    <rect x="482" y="306" width="120" height="40" rx="20" fill="#2C5A8C"/>
    <text x="542" y="332" fill="#FFFFFF">Kotlin</text>
    <rect x="614" y="306" width="196" height="40" rx="20" fill="#2C5A8C"/>
    <text x="712" y="332" fill="#FFFFFF">Jetpack Compose</text>
    <rect x="822" y="306" width="236" height="40" rx="20" fill="#2C5A8C"/>
    <text x="940" y="332" fill="#FFFFFF">Kotlin Multiplatform</text>
    <rect x="1070" y="306" width="148" height="40" rx="20" fill="#F5C842"/>
    <text x="1144" y="332" fill="#13233A">On-device AI</text>
  </g>
</svg>
'''


open('../assets/banner-v21.svg', 'w', encoding='utf-8', newline='\n').write(build())
open('preview.svg', 'w', encoding='utf-8', newline='\n').write(build(preview=True))
print(os.path.getsize('../assets/banner-v21.svg'))

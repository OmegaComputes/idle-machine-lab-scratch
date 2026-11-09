# Copyright 2026 Omega Compute
# SPDX-License-Identifier: CC-BY-4.0
"""Original flat SVG art for the Idle Machine Lab Scratch projects.
Simple, pastel, on-model colour pairs from the brand guide. Licence: CC BY 4.0 (art).
Character names and likenesses are trademarks/characters of Omega Compute and are not licensed; see NOTICE.
"""
P = dict(mint='#A9D8C5', rust='#A64F36', lilac='#B9A0D4', mustard='#B58B30', butter='#F0D98D', olive='#687447',
         coral='#E98579', teal='#237D80', cream='#F1E9D8', slate='#485767', ink='#2B2B3A', pearl='#F0EEE7',
         graphite='#30363C', kipgreen='#55D97B', silver='#B8BEC6', beige='#D9CDB4')

def _svg(w, h, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{body}</svg>'

def _face(cx, cy, skin):
    return (f'<circle cx="{cx}" cy="{cy}" r="22" fill="{skin}"/>'
            f'<circle cx="{cx-8}" cy="{cy+2}" r="2.6" fill="{P["ink"]}"/><circle cx="{cx+8}" cy="{cy+2}" r="2.6" fill="{P["ink"]}"/>'
            f'<path d="M{cx-7} {cy+11} Q{cx} {cy+16} {cx+7} {cy+11}" stroke="{P["ink"]}" stroke-width="2" fill="none" stroke-linecap="round"/>')

def juno():
    skin, hair = '#6B4430', '#1E1A1A'
    b = (f'<rect x="38" y="112" width="10" height="24" rx="4" fill="{P["ink"]}"/><rect x="52" y="112" width="10" height="24" rx="4" fill="{P["ink"]}"/>'
         f'<rect x="26" y="62" width="48" height="56" rx="14" fill="{P["mint"]}"/>'
         f'<rect x="26" y="96" width="48" height="8" fill="{P["rust"]}"/><rect x="46" y="62" width="8" height="50" fill="{P["rust"]}" opacity=".9"/>'
         f'<circle cx="50" cy="12" r="12" fill="{hair}"/><circle cx="40" cy="16" r="9" fill="{hair}"/><circle cx="60" cy="16" r="9" fill="{hair}"/>'
         f'<circle cx="50" cy="38" r="24" fill="{hair}"/>' + _face(50, 42, skin))
    return _svg(100, 140, b)

def dex():
    skin, hair = '#E8C4A8', '#6B4A32'
    b = (f'<rect x="38" y="112" width="10" height="24" rx="4" fill="{P["slate"]}"/><rect x="52" y="112" width="10" height="24" rx="4" fill="{P["slate"]}"/>'
         f'<rect x="24" y="62" width="52" height="56" rx="16" fill="{P["lilac"]}"/><rect x="38" y="90" width="24" height="12" rx="4" fill="#A88CC6"/>'
         f'<circle cx="50" cy="38" r="24" fill="{hair}"/>' + _face(50, 44, skin) +
         f'<path d="M26 34 Q50 8 74 34 Z" fill="{P["mustard"]}"/><rect x="50" y="30" width="30" height="6" rx="3" fill="{P["mustard"]}"/>')
    return _svg(100, 140, b)

def pia():
    skin, hair = '#E6BE9A', '#5A3B28'
    b = (f'<path d="M30 100 L22 138 L78 138 L70 100 Z" fill="{P["olive"]}"/>'
         f'<rect x="26" y="62" width="48" height="46" rx="14" fill="{P["butter"]}"/><rect x="26" y="62" width="10" height="46" rx="5" fill="{P["olive"]}" opacity=".85"/>'
         f'<path d="M70 30 Q90 60 78 92" stroke="{hair}" stroke-width="12" fill="none" stroke-linecap="round"/>'
         f'<circle cx="74" cy="40" r="5" fill="{P["olive"]}"/>'
         f'<circle cx="50" cy="38" r="24" fill="{hair}"/>' + _face(50, 44, skin))
    return _svg(100, 140, b)

def rollo():
    skin, hair = '#E9C3A0', '#141414'
    b = (f'<rect x="36" y="110" width="12" height="26" rx="4" fill="{P["teal"]}"/><rect x="52" y="110" width="12" height="26" rx="4" fill="{P["teal"]}"/>'
         f'<rect x="24" y="62" width="52" height="54" rx="16" fill="{P["coral"]}"/>'
         f'<rect x="24" y="106" width="52" height="8" rx="4" fill="{P["teal"]}"/><rect x="40" y="62" width="20" height="6" rx="3" fill="{P["teal"]}"/>'
         f'<path d="M26 40 Q26 14 50 14 Q74 14 74 40 L74 30 Q50 22 26 30 Z" fill="{hair}"/>' + _face(50, 44, skin) +
         f'<path d="M28 34 Q50 20 72 34 L72 28 Q50 12 28 28 Z" fill="{hair}"/>')
    return _svg(100, 140, b)

def kip():
    b = (f'<rect x="36" y="104" width="12" height="32" rx="5" fill="{P["graphite"]}"/><rect x="52" y="104" width="12" height="32" rx="5" fill="{P["graphite"]}"/>'
         f'<rect x="26" y="58" width="48" height="52" rx="14" fill="{P["pearl"]}" stroke="{P["graphite"]}" stroke-width="2"/>'
         f'<rect x="38" y="70" width="24" height="4" rx="2" fill="{P["silver"]}"/>'
         f'<path d="M20 64 q-8 12 0 20 q8 8 0 18" stroke="{P["mint"]}" stroke-width="3" fill="none"/>'
         f'<rect x="28" y="12" width="44" height="42" rx="18" fill="{P["pearl"]}" stroke="{P["graphite"]}" stroke-width="2"/>'
         f'<rect x="33" y="22" width="34" height="20" rx="10" fill="{P["graphite"]}"/>'
         f'<circle cx="43" cy="32" r="5" fill="{P["kipgreen"]}"/><circle cx="57" cy="32" r="5" fill="{P["kipgreen"]}"/>')
    return _svg(100, 140, b)

def machine(light='mint', label=''):
    lc = P.get(light, light)
    b = (f'<rect x="10" y="6" width="60" height="96" rx="6" fill="{P["beige"]}" stroke="{P["slate"]}" stroke-width="3"/>'
         f'<rect x="18" y="16" width="44" height="8" rx="2" fill="#BFB297"/><rect x="18" y="30" width="44" height="8" rx="2" fill="#BFB297"/>'
         f'<circle cx="24" cy="88" r="6" fill="{lc}" stroke="{P["slate"]}" stroke-width="1.5"/>'
         f'<rect x="36" y="84" width="26" height="6" rx="2" fill="{P["slate"]}"/>'
         + (f'<text x="40" y="66" font-family="monospace" font-size="16" text-anchor="middle" fill="{P["slate"]}">{label}</text>' if label else ''))
    return _svg(80, 108, b)

def lamp(on=True):
    glow = f'<circle cx="40" cy="30" r="28" fill="{P["butter"]}" opacity=".55"/>' if on else ''
    b = (glow + f'<rect x="36" y="44" width="8" height="70" fill="{P["slate"]}"/>'
         f'<circle cx="40" cy="30" r="16" fill="{P["butter"] if on else "#4A4A55"}" stroke="{P["slate"]}" stroke-width="3"/>'
         f'<rect x="24" y="112" width="32" height="8" rx="3" fill="{P["slate"]}"/>')
    return _svg(80, 124, b)

def board(title='JOB BOARD'):
    b = (f'<rect x="4" y="4" width="132" height="92" rx="8" fill="{P["cream"]}" stroke="{P["olive"]}" stroke-width="4"/>'
         f'<text x="70" y="28" font-family="monospace" font-size="15" text-anchor="middle" fill="{P["ink"]}">{title}</text>'
         + ''.join(f'<rect x="{14+i*30}" y="40" width="24" height="18" rx="2" fill="{c}"/>' for i, c in enumerate([P["mint"], P["lilac"], P["butter"], P["coral"]]))
         + ''.join(f'<rect x="{14+i*30}" y="64" width="24" height="18" rx="2" fill="{c}"/>' for i, c in enumerate([P["coral"], P["mint"], P["lilac"], P["butter"]])))
    return _svg(140, 100, b)

def door(open_=False):
    b = (f'<rect x="10" y="6" width="70" height="120" rx="4" fill="{P["slate"]}"/>'
         + (f'<rect x="16" y="12" width="58" height="114" fill="{P["butter"]}" opacity=".8"/>' if open_ else
            f'<rect x="16" y="12" width="58" height="114" fill="{P["teal"]}"/><circle cx="64" cy="70" r="4" fill="{P["silver"]}"/>'))
    return _svg(90, 130, b)

def clinic():
    b = (f'<rect x="6" y="30" width="108" height="70" rx="4" fill="{P["cream"]}" stroke="{P["slate"]}" stroke-width="3"/>'
         f'<path d="M0 34 L60 4 L120 34 Z" fill="{P["coral"]}"/>'
         f'<rect x="50" y="44" width="20" height="20" fill="{P["mint"]}"/><rect x="56" y="38" width="8" height="32" fill="#FFFFFF"/><rect x="44" y="50" width="32" height="8" fill="#FFFFFF"/>'
         f'<rect x="50" y="74" width="20" height="26" fill="{P["teal"]}"/>')
    return _svg(120, 104, b)

def hub():
    b = (f'<circle cx="40" cy="40" r="34" fill="{P["lilac"]}" stroke="{P["slate"]}" stroke-width="4"/>'
         f'<text x="40" y="47" font-family="monospace" font-size="18" text-anchor="middle" fill="{P["ink"]}">HUB</text>')
    return _svg(80, 80, b)

def button(text, colour='mint'):
    w = 24 + 11 * len(text)
    b = (f'<rect x="2" y="2" width="{w-4}" height="40" rx="12" fill="{P.get(colour, colour)}" stroke="{P["slate"]}" stroke-width="3"/>'
         f'<text x="{w/2}" y="28" font-family="monospace" font-size="18" text-anchor="middle" fill="{P["ink"]}">{text}</text>')
    return _svg(w, 44, b)

def dot(colour='coral'):
    return _svg(20, 20, f'<circle cx="10" cy="10" r="8" fill="{P.get(colour, colour)}"/>')

# ---------- backdrops (480 x 360) ----------
def _stripes():
    cols = ['mint', 'rust', 'lilac', 'mustard', 'butter', 'olive', 'coral', 'teal']
    return ''.join(f'<rect x="{i*60}" y="0" width="60" height="8" fill="{P[c]}"/>' for i, c in enumerate(cols))

def bd_lab():
    b = (f'<rect width="480" height="360" fill="{P["mint"]}"/><rect y="250" width="480" height="110" fill="#C9B79A"/>'
         f'<rect x="300" y="60" width="140" height="90" rx="6" fill="{P["cream"]}" stroke="{P["slate"]}" stroke-width="4"/>'
         f'<text x="370" y="112" font-family="monospace" font-size="20" text-anchor="middle" fill="{P["slate"]}">CORNER LAB</text>'
         f'<rect x="40" y="200" width="200" height="14" fill="{P["slate"]}"/>' + _stripes())
    return _svg(480, 360, b)

def bd_street(night=True):
    sky = '#2E3A55' if night else '#CFE6F0'
    win = P['butter'] if night else P['cream']
    houses = ''.join(f'<rect x="{x}" y="{y}" width="{w}" height="{300-y}" fill="{c}"/>'
                     + ''.join(f'<rect x="{x+12+j*26}" y="{y+18}" width="14" height="18" fill="{win}"/>' for j in range(max(1, (w-20)//26)))
                     for x, y, w, c in [(0, 170, 110, '#6E5A66'), (110, 140, 120, '#5E6B73'), (230, 180, 100, '#7A5E52'), (330, 150, 150, '#5A5F6E')])
    b = f'<rect width="480" height="360" fill="{sky}"/>' + houses + f'<rect y="300" width="480" height="60" fill="#3B3F48"/>' + _stripes()
    return _svg(480, 360, b)

def bd_grid():
    lines = ''.join(f'<line x1="{x}" y1="0" x2="{x}" y2="360" stroke="#D6CDB8" stroke-width="2"/>' for x in range(0, 481, 60))
    lines += ''.join(f'<line x1="0" y1="{y}" x2="480" y2="{y}" stroke="#D6CDB8" stroke-width="2"/>' for y in range(0, 361, 60))
    return _svg(480, 360, f'<rect width="480" height="360" fill="{P["cream"]}"/>' + lines + _stripes())

def bd_maze():
    walls = [(120, 0, 20, 240), (240, 120, 20, 240), (360, 0, 20, 240)]
    w = ''.join(f'<rect x="{x}" y="{y}" width="{ww}" height="{hh}" fill="{P["slate"]}"/>' for x, y, ww, hh in walls)
    return _svg(480, 360, f'<rect width="480" height="360" fill="{P["cream"]}"/>' + w +
                f'<text x="60" y="345" font-family="monospace" font-size="16" text-anchor="middle" fill="{P["slate"]}">START</text>' + _stripes())

def bd_plain(colour='cream'):
    return _svg(480, 360, f'<rect width="480" height="360" fill="{P.get(colour, colour)}"/>' + _stripes())

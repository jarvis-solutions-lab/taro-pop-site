# -*- coding: utf-8 -*-
"""Ilustraciones SVG de la página «Cómo catar tu muestra».

Son SVG en línea: pesan casi nada, se ven nítidas en cualquier pantalla y el
contorno usa currentColor, así que se adaptan al modo claro y oscuro. Las usan
build.py (la página) y generar_infografia_cata.py (la imagen para WhatsApp).
"""

TARO = "#a07bd4"      # polvo
PASTA = "#8a5cc4"     # polvo disuelto
AGUA = "#cfe7f8"
LECHE = "#f8f0e4"
MARCA = "#6a3fa0"

# Vaso: boca de 22 a 98 (y=24), fondo de 32 a 88 (y=140)
_VASO = "M22 24 L98 24 L88 140 Q87 146 81 146 L39 146 Q33 146 32 140 Z"


def _vaso(paso, contenido, extra="", badge=""):
    cid = f"vaso-{paso}"
    b = ""
    if badge:
        b = (f'<circle cx="104" cy="24" r="17" fill="{MARCA}"/>'
             f'<text x="104" y="28.5" text-anchor="middle" font-size="11.5" font-weight="800" '
             f'fill="#fff" font-family="Plus Jakarta Sans,system-ui,sans-serif">{badge}</text>')
    return (f'<svg class="cata-cup" viewBox="0 0 124 156" role="img" aria-hidden="true">'
            f'<defs><clipPath id="{cid}"><path d="{_VASO}"/></clipPath>'
            f'<linearGradient id="mezcla-{paso}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="#eadcf8"/><stop offset="1" stop-color="#b08ad9"/></linearGradient></defs>'
            f'{extra}'
            f'<g clip-path="url(#{cid})">{contenido}</g>'
            f'<path d="{_VASO}" fill="none" stroke="currentColor" stroke-width="3" stroke-linejoin="round"/>'
            f'{b}</svg>')


def _montana(y=122):
    return (f'<path d="M20 150 L20 140 Q40 {y - 14} 60 {y - 16} Q80 {y - 14} 100 140 L100 150 Z" fill="{TARO}"/>'
            f'<circle cx="48" cy="{y + 4}" r="2" fill="#fff" opacity=".5"/>'
            f'<circle cx="66" cy="{y + 1}" r="2" fill="#fff" opacity=".5"/>'
            f'<circle cx="58" cy="{y + 12}" r="2" fill="#fff" opacity=".5"/>')


def cup_svg(paso):
    """Vaso del paso 1 a 5 de la cata."""
    if paso == 1:
        cae = "".join(f'<circle cx="{x}" cy="{y}" r="2.4" fill="{TARO}"/>'
                      for x, y in [(56, 2), (64, 9), (59, 15), (52, 11), (67, 0)])
        return _vaso(1, _montana(), cae, "30 g")
    if paso == 2:
        vapor = "".join(f'<path d="M{x} 18 q-6 -6 0 -11 q6 -5 0 -11" fill="none" stroke="#b9a6d9" '
                        f'stroke-width="2.6" stroke-linecap="round"/>' for x in (46, 60, 74))
        return _vaso(2, _montana(124) + f'<rect x="0" y="100" width="124" height="60" fill="{AGUA}" opacity=".8"/>',
                     vapor, "85°")
    if paso == 3:
        giro = (f'<path d="M40 112 q20 -10 40 0 q-20 10 -36 2" fill="none" stroke="#fff" stroke-width="2.4" '
                f'stroke-linecap="round" opacity=".8"/>')
        cuchara = ('<line x1="96" y1="-6" x2="66" y2="118" stroke="#9c98a8" stroke-width="5" stroke-linecap="round"/>'
                   '<ellipse cx="66" cy="120" rx="6" ry="9" fill="#9c98a8" transform="rotate(14 66 120)"/>')
        return _vaso(3, f'<rect x="0" y="100" width="124" height="60" fill="{PASTA}"/>' + giro + cuchara,
                     "", "30 s")
    if paso == 4:
        chorro = (f'<rect x="57" y="-4" width="8" height="70" rx="4" fill="{LECHE}" stroke="#e2d4c1" '
                  f'stroke-width="1.2"/>')
        cont = (f'<rect x="0" y="66" width="124" height="90" fill="{LECHE}"/>'
                f'<rect x="0" y="104" width="124" height="60" fill="{PASTA}"/>'
                f'<path d="M0 106 Q20 96 40 104 T80 102 T124 104 L124 110 L0 110 Z" fill="{PASTA}" opacity=".55"/>')
        return _vaso(4, cont, chorro, "100")
    # paso 5: hielo y listo
    hielo = "".join(f'<rect x="{x}" y="{y}" width="22" height="20" rx="5" fill="#fff" fill-opacity=".75" '
                    f'stroke="#c9d9ea" stroke-width="1.6" transform="rotate({r} {x + 11} {y + 10})"/>'
                    for x, y, r in [(30, 52, -12), (54, 58, 8), (74, 50, -6), (40, 76, 14)])
    pitillo = f'<rect x="72" y="-10" width="9" height="140" rx="4.5" fill="{MARCA}" transform="rotate(12 76 60)"/>'
    cont = f'<rect x="0" y="48" width="124" height="110" fill="url(#mezcla-5)"/>' + hielo
    return _vaso(5, cont, pitillo, "✓")


def milk_scale_svg(ml, tope=180):
    """Vasito para la escala de leche: más leche, color más claro y vaso más lleno."""
    t = (ml - 100) / (tope - 100)                     # 0 → 1
    nivel = 96 - 38 * t                               # más alto con más leche
    claro = int(0x8a + (0xe6 - 0x8a) * t), int(0x5c + (0xd6 - 0x5c) * t), int(0xc4 + (0xf4 - 0xc4) * t)
    color = "#%02x%02x%02x" % claro
    cid = f"esc-{ml}"
    return (f'<svg class="cata-scale-cup" viewBox="0 0 124 156" aria-hidden="true">'
            f'<defs><clipPath id="{cid}"><path d="{_VASO}"/></clipPath></defs>'
            f'<g clip-path="url(#{cid})"><rect x="0" y="{nivel:.0f}" width="124" height="80" fill="{color}"/></g>'
            f'<path d="{_VASO}" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linejoin="round"/></svg>')


_ICON = ('<svg class="cata-icon" viewBox="0 0 48 48" aria-hidden="true" fill="none" stroke="currentColor" '
         'stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">{}</svg>')

ICONOS = {
    # Lo que necesitas
    "polvo": _ICON.format(f'<path d="M12 18h24l-3 22a3 3 0 0 1-3 2.6H18a3 3 0 0 1-3-2.6z"/>'
                          f'<path d="M15 18c0-6 4-10 9-10s9 4 9 10" fill="{TARO}" stroke="none" opacity=".9"/>'
                          f'<path d="M15 18c0-6 4-10 9-10s9 4 9 10"/><path d="M19 26h10" opacity=".5"/>'),
    "agua": _ICON.format('<path d="M10 22h22v14a6 6 0 0 1-6 6H16a6 6 0 0 1-6-6z"/>'
                         '<path d="M32 26h3a4 4 0 0 1 0 8h-3"/><path d="M15 22l3-6h8l3 6"/>'
                         '<path d="M16 12q-2-3 0-6M22 12q-2-3 0-6M28 12q-2-3 0-6" stroke="#b9a6d9"/>'
                         '<circle cx="40" cy="12" r="2.5" stroke="#e0703a"/><path d="M40 4v5.5" stroke="#e0703a"/>'),
    "leche": _ICON.format(f'<path d="M16 14h16v26a2 2 0 0 1-2 2H18a2 2 0 0 1-2-2z" fill="{LECHE}"/>'
                          '<path d="M16 14l3-7h10l3 7"/><path d="M19 7V4h10v3"/>'
                          '<path d="M16 26c3-2 5 2 8 0s5-2 8 0" stroke="#7fb3e6"/>'),
    "hielo": _ICON.format('<path d="M11 10h26l-3 30a2 2 0 0 1-2 2H16a2 2 0 0 1-2-2z"/>'
                          '<rect x="16" y="16" width="8" height="8" rx="2" stroke="#7fb3e6"/>'
                          '<rect x="25" y="22" width="8" height="8" rx="2" stroke="#7fb3e6"/>'
                          '<path d="M33 4l-3 34" stroke="#6a3fa0"/>'),
    # Recomendaciones
    "te": _ICON.format('<path d="M10 38C10 20 22 9 40 8c0 18-10 30-26 30z" fill="#bfe3c8" stroke="#3f8a55"/>'
                       '<path d="M10 38c8-10 16-17 24-22" stroke="#3f8a55"/>'),
    "ojos": _ICON.format(f'<path d="M12 8h24l-3 32a2 2 0 0 1-2 2H17a2 2 0 0 1-2-2z"/>'
                         f'<path d="M14 20h20l-1 9H15z" fill="{LECHE}" stroke="none"/>'
                         f'<path d="M15 29c4-3 6 2 9-1s6-3 9 0l-1 11H16z" fill="{TARO}" stroke="none"/>'
                         f'<path d="M14 20q5 4 10 1t10 2" stroke="{PASTA}"/>'),
    "toppings": _ICON.format('<circle cx="15" cy="30" r="6" fill="#3b2a26" stroke="none"/>'
                             '<circle cx="28" cy="33" r="6" fill="#3b2a26" stroke="none"/>'
                             '<circle cx="22" cy="20" r="6" fill="#f2a65a" stroke="none"/>'
                             '<circle cx="36" cy="21" r="6" fill="#e86b8a" stroke="none"/>'
                             '<circle cx="20" cy="18" r="1.6" fill="#fff" stroke="none"/>'
                             '<circle cx="34" cy="19" r="1.6" fill="#fff" stroke="none"/>'),
    "receta": _ICON.format(f'<path d="M24 6l4 10 10 4-10 4-4 10-4-10-10-4 10-4z" fill="{TARO}" stroke="{MARCA}"/>'
                           '<path d="M38 32l1.6 4 4 1.6-4 1.6-1.6 4-1.6-4-4-1.6 4-1.6z" fill="#f2c94c" stroke="none"/>'),
}

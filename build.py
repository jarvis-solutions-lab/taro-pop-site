# -*- coding: utf-8 -*-
"""Generador del sitio estático Insumos Pop."""
import html as html_mod
import json, os, shutil, urllib.parse
from data import WA, WA_DISPLAY, SITE, DOMAIN, POWDERS, FRUIT_POWDER, SYRUP, RECIPES, PROFILES

RAIZ = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(RAIZ, "site")
TODAY = "2026-08-14"


def preparar_assets():
    """Copia las imágenes, el CSS y el JS al sitio generado.

    Busca la carpeta 'assets' donde esté: en la raíz del proyecto (lo normal)
    o dentro de site/. Así el proyecto funciona sin importar cómo se haya
    organizado el repositorio.
    """
    destino = os.path.join(OUT, "assets")
    for candidata in (os.path.join(RAIZ, "assets"), destino):
        if os.path.isdir(candidata):
            origen = candidata
            break
    else:
        print("AVISO: no encontré la carpeta 'assets' (imágenes, CSS y JS).")
        return
    os.makedirs(OUT, exist_ok=True)
    if os.path.abspath(origen) != os.path.abspath(destino):
        if os.path.isdir(destino):
            shutil.rmtree(destino)
        shutil.copytree(origen, destino)
    n = sum(len(f) for _, _, f in os.walk(destino))
    print(f"Assets listos: {n} archivos desde {os.path.relpath(origen, RAIZ)}/")


preparar_assets()

ALL_PRODUCTS = {p["slug"]: p for p in POWDERS}
ALL_PRODUCTS[FRUIT_POWDER["slug"]] = FRUIT_POWDER
ALL_PRODUCTS[SYRUP["slug"]] = SYRUP
RECIPES_BY_SLUG = {r["slug"]: r for r in RECIPES}

def product_url(slug):
    if slug == SYRUP["slug"]:
        return "siropes-bubble-tea/siropes-de-fruta/"
    return "polvos-bubble-tea/" + slug + "/"

def fmt_cop(n):
    return "$" + f"{n:,}".replace(",", ".")

def wa_link(msg):
    return "https://wa.me/" + WA + "?text=" + urllib.parse.quote(msg)

WA_GENERIC = wa_link("Hola Insumos Pop 👋 Quiero información sobre sus insumos de bubble tea para mi negocio.")

WA_ICON = ('<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
 '<path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2c-1.6 0-3.1-.4-4.4-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.6-6.1c-.3-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1-.2.3-.6.8-.8 1-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.4-3c-.3-.4 0-.5.1-.7l.4-.5c.1-.2.1-.3.2-.5 0-.2 0-.4-.1-.5l-.8-1.9c-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.5.1-.7.3-.2.3-.9.9-.9 2.2s.9 2.5 1.1 2.7c.1.2 1.8 2.8 4.4 3.9.6.3 1.1.4 1.5.6.6.2 1.2.2 1.6.1.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.2-.3-.2-.6-.4z"/></svg>')

def head(title, desc, canonical, root, jsonld=None, og_img=None, preload=None):
    j = ""
    if jsonld:
        for block in jsonld:
            j += '<script type="application/ld+json">' + json.dumps(block, ensure_ascii=False) + "</script>\n"
    og = og_img or (SITE + "/assets/img/polvo-taro-bubble-tea.webp")
    pre = f'<link rel="preload" as="image" href="{preload}">' if preload else ""
    return f"""<!doctype html>
<html lang="es-CO" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Insumos Pop">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{og}">
<meta property="og:url" content="{canonical}">
<meta name="theme-color" content="#faf7f0">
<script>(function(){{try{{var t=localStorage.getItem("ip_theme_v2");if(t==="dark"){{document.documentElement.setAttribute("data-theme","dark");document.querySelector('meta[name="theme-color"]').setAttribute("content","#0b0b0f");}}}}catch(e){{}}}})()</script>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ccircle cx='50' cy='50' r='46' fill='%230b0b0f'/%3E%3Ccircle cx='50' cy='50' r='45' fill='none' stroke='%23d8b46a' stroke-width='4'/%3E%3Ctext x='50' y='66' font-size='48' text-anchor='middle' fill='%23d8b46a' font-family='Arial' font-weight='bold'%3EIP%3C/text%3E%3C/svg%3E">
{pre}
<link rel="stylesheet" href="{root}assets/styles.css">
{j}</head>
"""

NAV_ITEMS = [
    ("polvos", "polvos-bubble-tea/", "Polvos"),
    ("siropes", "siropes-bubble-tea/", "Siropes"),
    ("recetas", "recetas-bubble-tea/", "Recetas"),
    ("guia", "guia-emprender-bubble-tea/", "Guía para emprender"),
    ("nosotros", "nosotros/", "Nosotros"),
]

def header_html(root, current="", body_class=""):
    items = ""
    for key, href, label in NAV_ITEMS:
        cur = ' aria-current="page"' if key == current else ""
        items += f'<li><a href="{root}{href}"{cur}>{label}</a></li>'
    cls = f' class="{body_class}"' if body_class else ""
    return f"""<body data-root="{root}"{cls}>
<a class="skip" href="#main">Saltar al contenido</a>
<header class="site">
  <div class="wrap nav">
    <a class="brand" href="{root}">Insumos <span>Pop</span></a>
    <a class="btn btn-gold nav-cta-mobile" href="{root}cotizar/">Cotizar</a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="nav-links">☰ Menú</button>
    <ul class="nav-links" id="nav-links">
      {items}
      <li><a class="nav-cta" href="{root}cotizar/">Cotizar para mi negocio</a></li>
    </ul>
    <button class="theme-toggle" aria-label="Cambiar a modo claro">☀️</button>
  </div>
</header>
<main id="main">
"""

def footer_html(root, wa_url=None):
    wa = wa_url or WA_GENERIC
    return f"""</main>
<footer class="site">
  <div class="wrap foot">
    <div>
      <p class="brand" style="font-size:1.3rem">Insumos <span class="gold">Pop</span></p>
      <p class="muted">Sabores premium de Asia para negocios en Colombia. Importación directa de Taiwán, sin intermediarios: de la fábrica a tu local.</p>
      <p><a class="btn btn-wa" href="{wa}" target="_blank" rel="noopener">{WA_ICON} WhatsApp {WA_DISPLAY}</a></p>
    </div>
    <div>
      <h3>Catálogo</h3>
      <ul>
        <li><a href="{root}polvos-bubble-tea/">Polvos para bubble tea</a></li>
        <li><a href="{root}siropes-bubble-tea/">Siropes de fruta</a></li>
        <li><a href="{root}recetas-bubble-tea/">Recetas</a></li>
        <li><a href="{root}guia-emprender-bubble-tea/">Guía para emprender</a></li>
      </ul>
    </div>
    <div>
      <h3>Para tu negocio</h3>
      <ul>
        {"".join(f'<li><a href="{root}{pr["slug"]}/">{pr["label"]}</a></li>' for pr in PROFILES)}
      </ul>
    </div>
    <div>
      <h3>Ayuda</h3>
      <ul>
        <li><a href="{root}cotizar/">Cotizar</a></li>
        <li><a href="{root}envios-y-pagos/">Envíos y pagos</a></li>
        <li><a href="{root}preguntas-frecuentes/">Preguntas frecuentes</a></li>
        <li><a href="{root}nosotros/">Nosotros</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap legal">Distribuido por Insumos Pop bajo la razón social de Taro Pop S.A.S. · Colombia · WhatsApp {WA_DISPLAY}</div>
</footer>
<a class="wa-float" href="{wa}" target="_blank" rel="noopener" aria-label="Escribir por WhatsApp">
  <svg width="30" height="30" viewBox="0 0 24 24" fill="#06230f" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2c-1.6 0-3.1-.4-4.4-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.6-6.1c-.3-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1-.2.3-.6.8-.8 1-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.4-3c-.3-.4 0-.5.1-.7l.4-.5c.1-.2.1-.3.2-.5 0-.2 0-.4-.1-.5l-.8-1.9c-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.5.1-.7.3-.2.3-.9.9-.9 2.2s.9 2.5 1.1 2.7c.1.2 1.8 2.8 4.4 3.9.6.3 1.1.4 1.5.6.6.2 1.2.2 1.6.1.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.2-.3-.2-.6-.4z"/></svg>
</a>
<div class="quote-bar">
  <span class="qb-text" aria-live="polite"></span>
  <a class="btn btn-gold" href="{root}cotizar/">Completar cotización</a>
</div>
<div class="toast" role="status" aria-live="polite"></div>
<script src="{root}assets/site.js" defer></script>
</body>
</html>
"""

def write_page(relpath, html):
    path = os.path.join(OUT, relpath)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

def add_btn(p, root, cls="btn-line"):
    return (f'<button class="btn {cls}" data-add="{p["sku"]}" data-name="{p["name"]}" '
            f'data-price="{p["price"]}" data-format="{p["format"]}" '
            f'data-img="assets/img/{p["img"]}-card.webp">Agregar a cotización</button>')

def card(p, root):
    url = root + product_url(p["slug"])
    uses = " · ".join(p["uses"][:2])
    if p.get("flavors"):
        # Los productos con sabores se eligen en la ficha (evita pedidos sin sabor)
        actions = f'<a class="btn btn-gold" href="{url}">Elegir sabores</a>'
    else:
        actions = f'{add_btn(p, root, "btn-gold")}<a class="btn btn-line" href="{url}">Ver ficha</a>'
    return f"""<article class="card">
  <a class="card-img" href="{url}" aria-hidden="true" tabindex="-1"><img src="{root}assets/img/{p['img']}-card.webp" alt="{p['alt']}" loading="lazy" width="520" height="546"></a>
  <div class="card-body">
    <h3><a href="{url}">{p['short']}</a> <span class="zh">{p['zh']}</span></h3>
    <p class="meta">{p['format']} · {uses}</p>
    <p class="price">{fmt_cop(p['price'])} <small>IVA incluido</small></p>
    <div class="card-actions">
      {actions}
    </div>
  </div>
</article>"""

def breadcrumb(root, items):
    lis = f'<li><a href="{root}">Inicio</a></li>'
    for href, label in items[:-1]:
        lis += f'<li><a href="{root}{href}">{label}</a></li>'
    lis += f"<li aria-current='page'>{items[-1][1]}</li>"
    return f'<nav class="breadcrumb wrap" aria-label="Ruta de navegación"><ol>{lis}</ol></nav>'

def breadcrumb_ld(items):
    els = [{"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE + "/"}]
    for i, (href, label) in enumerate(items):
        els.append({"@type": "ListItem", "position": i + 2, "name": label,
                    "item": SITE + "/" + href if href else None})
    for e in els:
        if e.get("item") is None:
            del e["item"]
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": els}

def product_ld(p):
    return {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": p["name"],
        "image": SITE + "/assets/img/" + p["img"] + ".webp",
        "description": p["teaser"],
        "sku": p["sku"],
        "brand": {"@type": "Brand", "name": "Insumos Pop"},
        "category": "Insumos para bubble tea",
        "offers": {
            "@type": "Offer",
            "url": SITE + "/" + product_url(p["slug"]),
            "priceCurrency": "COP",
            "price": str(p["price"]),
            "itemCondition": "https://schema.org/NewCondition",
            "seller": {"@type": "Organization", "name": "Insumos Pop"},
        },
    }

def faq_html(faqs):
    out = ""
    for q, a in faqs:
        out += f'<details class="faq"><summary>{q}</summary><p>{a}</p></details>'
    return out

def kit_attr(items):
    data = []
    for slug, qty, name_suffix in items:
        p = ALL_PRODUCTS[slug]
        key = p["sku"] + ("-eleccion" if name_suffix else "")
        data.append({"key": key, "name": p["name"] + (name_suffix or ""), "price": p["price"],
                     "format": p["format"], "img": f"assets/img/{p['img']}-card.webp", "qty": qty})
    return html_mod.escape(json.dumps(data, ensure_ascii=False), quote=True)

def kit_price(items):
    return sum(ALL_PRODUCTS[slug]["price"] * qty for slug, qty, _ in items)

def kit_html(kit, root="./", img_slug=None, show_title=True):
    lis = ""
    for slug, qty, suffix in kit["items"]:
        p = ALL_PRODUCTS[slug]
        q = f"{qty} × " if qty > 1 else ""
        lis += f"<li>{q}{p['short']} · {p['format'].replace('Bolsa ', '').replace('Botella ', '')}{suffix or ''}</li>"
    total = kit_price(kit["items"])
    img = ""
    if img_slug:
        ip = ALL_PRODUCTS[img_slug]
        img = f'<img src="{root}assets/img/{ip["img"]}-card.webp" alt="" loading="lazy">'
    wa_kit = wa_link(f"Hola Insumos Pop 👋 Quiero cotizar el {kit['name']} ({fmt_cop(total)}, IVA incluido). Mi ciudad: ")
    title = f"<h3>{kit['name']}</h3>" if show_title else ""
    return f"""<div class="kit">
      {img}
      {title}
      <p class="muted">{kit['pitch']}</p>
      <ul>{lis}</ul>
      <p class="kit-price">{fmt_cop(total)} <small>IVA incluido</small></p>
      <p class="kit-note">Es la suma exacta de los precios del catálogo: lo que agregamos es la selección ya pensada y la asesoría para montarla.</p>
      <div class="kit-cta">
        <a class="btn btn-wa" href="{wa_kit}" target="_blank" rel="noopener">{WA_ICON} Cotizar este kit</a>
        <button class="btn btn-line" data-kit="{kit_attr(kit['items'])}">Agregar a cotización</button>
      </div>
    </div>"""

# perfiles a los que apunta cada producto (chips "Ideal para" en fichas)
AUDIENCES = {
    "polvo-taro": ["proveedor-bubble-tea", "kit-emprendedor-bubble-tea"],
    "polvo-okinawa-brown-sugar": ["proveedor-bubble-tea"],
    "polvo-thai-milk-tea": ["proveedor-bubble-tea"],
    "polvo-hokkaido-milk-tea": ["proveedor-bubble-tea", "kit-emprendedor-bubble-tea"],
    "polvo-cheese-foam": ["bubble-tea-para-cafeterias", "siropes-para-cocteleria"],
    "polvo-coral-azul": ["siropes-para-cocteleria", "proveedor-bubble-tea"],
    "polvo-matcha-taiwan": ["bubble-tea-para-cafeterias"],
    "matcha-shizuoka": ["bubble-tea-para-cafeterias"],
    "polvo-hojicha": ["bubble-tea-para-cafeterias"],
    "hojicha-puro": ["bubble-tea-para-cafeterias"],
    "polvos-de-fruta": ["kit-emprendedor-bubble-tea"],
    "siropes-de-fruta": ["siropes-para-cocteleria"],
}
PROFILE_BY_SLUG = {pr["slug"]: pr for pr in PROFILES}

def audience_chips(p, root):
    slugs = AUDIENCES.get(p["slug"], [])
    if not slugs:
        return ""
    links = " · ".join(f'<a href="{root}{s}/">{PROFILE_BY_SLUG[s]["label"]}</a>' for s in slugs)
    return f'<p class="sample-note">Ideal para: {links}</p>'

def related_html(p, root):
    cards = "".join(card(ALL_PRODUCTS[s], root) for s in p.get("related", []) if s in ALL_PRODUCTS)
    if not cards:
        return ""
    return f'<section class="wrap"><h2>También te puede interesar</h2><div class="grid">{cards}</div></section>'

def recipes_links(p, root):
    links = [r for r in p.get("recipes", []) if r in RECIPES_BY_SLUG]
    if not links:
        return ""
    lis = "".join(f'<li><a href="{root}recetas-bubble-tea/{s}/">{RECIPES_BY_SLUG[s]["title"]}</a></li>' for s in links)
    return f'<h2>Recetas con este producto</h2><ul class="list">{lis}</ul>'

# ---------------------------------------------------------------- fichas
COMPARE = {}
_cmp_matcha = """<div class="compare"><h3>¿Cuál matcha te conviene?</h3>
<p><strong>Mezcla lista (Taiwan Matcha, $95.000 · 1 kg):</strong> servicio rápido, sabor ya balanceado y costo por bebida controlado. Ideal para volumen.</p>
<p><strong>100% puro (Shizuoka Matcha, $110.000 · 500 g):</strong> tú controlas dosis, leche y dulzor; carta de especialidad con historia de origen real.</p>
<p class="muted">¿Cuál pido? Si vendes volumen, la mezcla; si tu carta es de autor, el puro — o ambos: uno para la carta base y otro para especiales.</p></div>"""
_cmp_hojicha = """<div class="compare"><h3>¿Cuál hojicha te conviene?</h3>
<p><strong>Mezcla lista (Hojicha, $95.000 · 1 kg):</strong> lista para bebidas, servicio rápido y costo por vaso controlado.</p>
<p><strong>100% puro (Pure Hojicha, $110.000 · 500 g):</strong> té tostado single origin de Japón para lattes y postres de autor.</p>
<p class="muted">¿Cuál pido? Si vendes volumen, la mezcla; si tu carta es de autor, el puro — o ambos.</p></div>"""
COMPARE["polvo-matcha-taiwan"] = _cmp_matcha
COMPARE["matcha-shizuoka"] = _cmp_matcha
COMPARE["polvo-hojicha"] = _cmp_hojicha
COMPARE["hojicha-puro"] = _cmp_hojicha

def cost_row(p):
    if p.get("grams"):
        per_g = p["price"] / p["grams"]
        per_g_txt = f"${per_g:,.0f}".replace(",", ".")
        return (f"<tr><th>Costo por gramo</th><td>Equivale a {per_g_txt} por gramo: multiplica por tu dosis "
                "por vaso y obtienes tu costo de insumo por bebida. Si quieres, te ayudamos a calcularlo por WhatsApp.</td></tr>")
    return ("<tr><th>Costo por litro</th><td>Equivale a ≈ $58.000 por litro de concentrado (botella de 1.9 L), "
            "y al ser concentrado, cada botella rinde muchas bebidas.</td></tr>")

def build_ficha(p, category_href, category_label, extra_gallery="", flavor_select=""):
    slug = p["slug"]
    url_rel = product_url(slug)
    root = "../../"
    canonical = SITE + "/" + url_rel
    wa_msg = wa_link(f"Hola Insumos Pop 👋 Quiero cotizar {p['name']} (SKU {p['sku']}, {p['format']}, {fmt_cop(p['price'])}) y recibir la ficha técnica con dosificación. Mi ciudad: ")
    crumbs = [(category_href, category_label), (url_rel, p["short"])]
    flavors_row = ""
    if p.get("flavors"):
        chips = "".join(f'<span class="chip on">{f}</span>' for f in p["flavors"])
        flavors_row = f'<h2>Sabores disponibles</h2><div class="chips">{chips}</div>'
    uses_chips = "".join(f'<span class="chip">{u}</span>' for u in p["uses"])
    desc_html = "".join(f"<p>{d}</p>" for d in p["desc"])
    spec_flavor = f"<tr><th>Sabores</th><td>{', '.join(p['flavors'])}</td></tr>" if p.get("flavors") else ""
    html = head(
        f"{p['name']} | {p['format']} · {fmt_cop(p['price'])} | Insumos Pop",
        f"{p['teaser']} {p['format']}, {fmt_cop(p['price'])} IVA incluido. Importación directa. Cotiza por WhatsApp para tu negocio en Colombia.",
        canonical, root,
        jsonld=[product_ld(p), breadcrumb_ld(crumbs)],
        og_img=SITE + "/assets/img/" + p["img"] + ".webp",
        preload=root + "assets/img/" + p["img"] + ".webp",
    )
    html += header_html(root, "polvos" if "polvos" in category_href else "siropes")
    html += breadcrumb(root, crumbs)
    html += f"""
<div class="wrap pdp">
  <div class="pdp-gallery">
    <img src="{root}assets/img/{p['img']}.webp" alt="{p['alt']}" width="1100" height="1155" id="pdp-main">
    {extra_gallery}
  </div>
  <div>
    <p class="eyebrow">{category_label}</p>
    <h1>{p['name']}</h1>
    <p class="zh">{p['zh']}</p>
    <hr class="rule">
    <p>{p['teaser']}</p>
    <div class="chips">{uses_chips}</div>
    {audience_chips(p, root)}
    <div class="price-box">
      <span class="big">{fmt_cop(p['price'])}</span> · {p['format']}
      <div class="cond">IVA incluido · Importación directa — confirma disponibilidad y tiempos de entrega por WhatsApp</div>
      <div class="cond"><strong class="gold">Muestra gratis para negocios</strong> disponible: pídela por WhatsApp antes de tu primer pedido.</div>
    </div>
    {flavor_select}
    <div class="cta-row">
      <a class="btn btn-wa" href="{wa_msg}" target="_blank" rel="noopener">{WA_ICON} Cotizar por WhatsApp</a>
      {add_btn(p, root)}
    </div>
  </div>
</div>
<section class="wrap">
  <div class="split">
    <div>
      <h2>Sobre este producto</h2>
      {desc_html}
      {COMPARE.get(slug, "")}
      {flavors_row}
      {recipes_links(p, root)}
    </div>
    <div>
      <h2>Especificaciones</h2>
      <table class="spec">
        <tr><th>Presentación</th><td>{p['format']}</td></tr>
        <tr><th>Precio</th><td>{fmt_cop(p['price'])} (IVA incluido)</td></tr>
        {spec_flavor}
        {cost_row(p)}
        <tr><th>Origen</th><td>{p['origin']}</td></tr>
        <tr><th>Nombre original</th><td>{p['zh']}</td></tr>
        <tr><th>Referencia (SKU)</th><td>{p['sku']}</td></tr>
        <tr><th>Conservación</th><td>Lugar fresco y seco, protegido de la luz y bien cerrado después de abrir.</td></tr>
        <tr><th>Dosis y rendimiento</th><td>Dependen de tu receta y tamaño de vaso. Escríbenos por WhatsApp y te compartimos la ficha técnica y dosificación recomendada.</td></tr>
      </table>
      <h2>Preguntas frecuentes</h2>
      {faq_html(p['faqs'])}
    </div>
  </div>
</section>
{related_html(p, root)}
"""
    html += footer_html(root)
    write_page(url_rel + "index.html", html)

for p in POWDERS:
    build_ficha(p, "polvos-bubble-tea/", "Polvos para bubble tea")

# Ficha polvos de fruta (con selector de sabor y segunda imagen)
fp = FRUIT_POWDER
extra = f"""<div class="pdp-thumbs">
  <img src="../../assets/img/{fp['img']}-card.webp" alt="{fp['alt']}" onclick="document.getElementById('pdp-main').src='../../assets/img/{fp['img']}.webp'">
  <img src="../../assets/img/{fp['img2']}-card.webp" alt="{fp['alt2']}" onclick="document.getElementById('pdp-main').src='../../assets/img/{fp['img2']}.webp'">
</div>"""
sel = "".join(f"<option>{f}</option>" for f in fp["flavors"])
flavor_sel = f"""<div class="field"><label for="sabor-fruta">Elige el sabor</label>
<select id="sabor-fruta" data-flavor-for="{fp['sku']}">{sel}</select></div>"""
build_ficha(fp, "polvos-bubble-tea/", "Polvos para bubble tea", extra_gallery=extra, flavor_select=flavor_sel)

# Ficha siropes (con 3 imágenes y selector)
sy = SYRUP
extra = f"""<div class="pdp-thumbs">
  <img src="../../assets/img/{sy['img']}-card.webp" alt="{sy['alt']}" onclick="document.getElementById('pdp-main').src='../../assets/img/{sy['img']}.webp'">
  <img src="../../assets/img/{sy['img2']}-card.webp" alt="{sy['alt2']}" onclick="document.getElementById('pdp-main').src='../../assets/img/{sy['img2']}.webp'">
  <img src="../../assets/img/{sy['img3']}-card.webp" alt="{sy['alt3']}" onclick="document.getElementById('pdp-main').src='../../assets/img/{sy['img3']}.webp'">
</div>"""
sel = "".join(f"<option>{f}</option>" for f in sy["flavors"])
flavor_sel = f"""<div class="field"><label for="sabor-sirope">Elige el sabor</label>
<select id="sabor-sirope" data-flavor-for="{sy['sku']}">{sel}</select></div>"""
build_ficha(sy, "siropes-bubble-tea/", "Siropes para bubble tea y bebidas", extra_gallery=extra, flavor_select=flavor_sel)

# ---------------------------------------------------------------- landings por perfil
def profile_webpage_ld(pr, canonical):
    return {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": pr["title"],
        "url": canonical,
        "inLanguage": "es-CO",
        "description": pr["metadesc"],
        "audience": {"@type": "BusinessAudience", "name": pr["label"]},
        "about": "Insumos para bubble tea y bebidas",
    }

def itemlist_ld(slugs):
    return {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1,
             "name": ALL_PRODUCTS[s]["name"],
             "url": SITE + "/" + product_url(s)}
            for i, s in enumerate(slugs)
        ],
    }

def profile_faq_ld(faqs):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs],
    }

def build_profile(pr):
    root = "../"
    url_rel = pr["slug"] + "/"
    canonical = SITE + "/" + url_rel
    hero_p = ALL_PRODUCTS[pr["hero_product"]]
    wa_url = wa_link(pr["wa_msg"])
    crumbs = [(url_rel, pr["label"])]
    trust = "".join(f"<div><b>{t}</b>{d}</div>" for t, d in pr["trust"])
    benefits = "".join(f'<div class="benefit"><h3>{t}</h3><p class="muted">{d}</p></div>'
                       for t, d in pr["benefits"])
    prod_cards = "".join(card(ALL_PRODUCTS[s], root) for s in pr["product_slugs"])
    menu_chips = "".join(f'<span class="chip on">{m}</span>' for m in pr["menu_ideas"])
    recipe_lis = "".join(
        f'<li><a href="{root}recetas-bubble-tea/{s}/">{RECIPES_BY_SLUG[s]["title"]}</a></li>'
        for s in pr["recipe_slugs"])
    sisters = " · ".join(f'<a href="{root}{o["slug"]}/">{o["label"]}</a>'
                         for o in PROFILES if o["slug"] != pr["slug"])
    html = head(
        pr["title"], pr["metadesc"], canonical, root,
        jsonld=[breadcrumb_ld(crumbs), profile_webpage_ld(pr, canonical),
                itemlist_ld(pr["product_slugs"]), profile_faq_ld(pr["faqs"])],
        og_img=SITE + "/assets/img/" + hero_p["img"] + ".webp",
        preload=root + "assets/img/" + hero_p["img"] + ".webp",
    )
    html += header_html(root, "", body_class="landing")
    html += breadcrumb(root, crumbs)
    html += f"""
<div class="hero">
  <div class="wrap hero-grid">
    <div>
      <p class="eyebrow">{pr['eyebrow']}</p>
      <h1>{pr['h1']}</h1>
      <p class="lead">{pr['lead']}</p>
      <div class="cta-row">
        <a class="btn btn-wa" href="{wa_url}" target="_blank" rel="noopener">{WA_ICON} {pr['cta_label']}</a>
        <a class="btn btn-line" href="{root}{pr['catalog_href']}">{pr['catalog_label']}</a>
      </div>
      <p class="sample-note">Pide tu <strong>muestra gratis para negocios</strong> por WhatsApp y prueba antes de tu primer pedido.</p>
      <div class="trust">{trust}</div>
    </div>
    <img src="{root}assets/img/{hero_p['img']}.webp" alt="{hero_p['alt']}" width="1100" height="1155" fetchpriority="high">
  </div>
</div>

<section class="wrap">
  <p class="eyebrow">Por qué funciona en tu negocio</p>
  <h2>Lo que ganas con Insumos Pop</h2>
  <hr class="rule">
  <div class="benefits">{benefits}</div>
  {pr['extra_html']}
</section>

<section class="wrap">
  <p class="eyebrow">La forma más rápida de empezar</p>
  <h2>{pr['kit']['name']}</h2>
  <hr class="rule">
  <div class="split" style="align-items:start">
    {kit_html(pr['kit'], root, pr['kit']['items'][-1][0], show_title=False)}
    <div class="panel">
      <p class="eyebrow">Así se ve en tu carta</p>
      <h3 style="font-size:1.35rem">Ideas de menú</h3>
      <div class="chips">{menu_chips}</div>
      <h3 style="margin-top:16px">Recetas paso a paso</h3>
      <ul class="list">{recipe_lis}</ul>
      <p class="muted" style="font-size:.92rem">¿Primera vez con estos insumos? <a href="{root}guia-emprender-bubble-tea/">Aprende el paso a paso en la guía para emprender</a>.</p>
    </div>
  </div>
</section>

<section class="wrap">
  <p class="eyebrow">Selección para ti</p>
  <h2>Productos recomendados</h2>
  <hr class="rule">
  <div class="grid">{prod_cards}</div>
</section>

<section class="wrap">
  <p class="eyebrow">Dudas de tu sector</p>
  <h2>Preguntas frecuentes</h2>
  <hr class="rule">
  <div style="max-width:760px">{faq_html(pr['faqs'])}</div>
  <p class="muted" style="margin-top:18px">¿Tu negocio es otro? Mira: {sisters}.</p>
</section>

<section class="cta-final">
  <div class="wrap center">
    <h2>{pr['cta_title']}</h2>
    <p class="muted" style="max-width:38em;margin:0 auto 8px">{pr['cta_text']}</p>
    <hr class="rule">
    <a class="btn btn-wa" href="{wa_url}" target="_blank" rel="noopener">{WA_ICON} {pr['cta_label']}</a>
  </div>
</section>
"""
    html += footer_html(root, wa_url)
    write_page(url_rel + "index.html", html)

for pr in PROFILES:
    build_profile(pr)

# ---------------------------------------------------------------- categoría polvos
root = "../"
canonical = SITE + "/polvos-bubble-tea/"
crumbs = [("polvos-bubble-tea/", "Polvos para bubble tea")]
premium_cards = "".join(card(p, root) for p in POWDERS)
html = head(
    "Polvos para Bubble Tea | Taro, Matcha, Hojicha y más | Insumos Pop",
    "Polvos premium para bubble tea importados directo de Taiwán: taro, matcha, hojicha, brown sugar, thai milk tea, cheese foam y polvos de fruta. Precios con IVA para negocios en Colombia.",
    canonical, root, jsonld=[breadcrumb_ld(crumbs)],
)
html += header_html(root, "polvos")
html += breadcrumb(root, crumbs)
html += f"""
<section class="wrap" style="padding-top:26px">
  <p class="eyebrow">Catálogo</p>
  <h1>Polvos para bubble tea</h1>
  <hr class="rule">
  <p style="max-width:46em">Polvos saborizados premium importados directo de Taiwán y Japón, sin intermediarios. Son la base de milk teas, frappés, lattes y postres: sabores que en Colombia no se conseguían, o solo en réplicas de baja calidad y sobreprecio.</p>
  <p class="muted" style="max-width:46em">Todos los precios incluyen IVA. ¿No sabes por dónde empezar? <a href="{root}guia-emprender-bubble-tea/">Mira la guía para armar tu menú</a> o <a href="{WA_GENERIC}" target="_blank" rel="noopener">escríbenos por WhatsApp</a>.</p>
  <h2 style="margin-top:34px">Joyas Premium <span class="muted" style="font-weight:500;font-size:1rem">· sabores ultra premium originales de Asia</span></h2>
  <div class="grid">{premium_cards}</div>
  <h2 style="margin-top:44px">Polvos de Fruta <span class="muted" style="font-weight:500;font-size:1rem">· 6 sabores asiáticos</span></h2>
  <div class="grid">{card(FRUIT_POWDER, root)}</div>
</section>
"""
html += footer_html(root)
write_page("polvos-bubble-tea/index.html", html)

# ---------------------------------------------------------------- categoría siropes
canonical = SITE + "/siropes-bubble-tea/"
crumbs = [("siropes-bubble-tea/", "Siropes para bubble tea")]
chips = "".join(f'<span class="chip on">{f}</span>' for f in SYRUP["flavors"])
html = head(
    "Siropes para Bubble Tea y Bebidas | 12 sabores | Insumos Pop",
    "Siropes concentrados de fruta hechos en Taiwán para bubble tea, cócteles, frappés, limonadas y sodas italianas. 12 sabores en botella de 1.9 L, $110.000 IVA incluido.",
    canonical, root, jsonld=[breadcrumb_ld(crumbs)],
)
html += header_html(root, "siropes")
html += breadcrumb(root, crumbs)
html += f"""
<section class="wrap" style="padding-top:26px">
  <p class="eyebrow">Catálogo</p>
  <h1>Siropes de fruta para bebidas</h1>
  <hr class="rule">
  <p style="max-width:46em">Concentrados de fruta nacidos en Taiwán, con sabor intenso, limpio y natural — sin el gusto artificial de los jarabes comunes. Un solo chorro transforma un cóctel, un frappé, un latte, una limonada o una soda italiana.</p>
  <p style="max-width:46em">Son concentrados de verdad: rinden muchísimo, así que tu carta gana sabor y tú cuidas el margen.</p>
  <h2 style="margin-top:30px">12 sabores disponibles</h2>
  <div class="chips">{chips}</div>
  <div class="grid" style="margin-top:22px;grid-template-columns:repeat(auto-fill,minmax(280px,1fr))">{card(SYRUP, root)}</div>
  <p style="margin-top:26px"><a class="btn btn-gold" href="{root}siropes-bubble-tea/siropes-de-fruta/">Ver ficha completa de los siropes</a></p>
</section>
"""
html += footer_html(root)
write_page("siropes-bubble-tea/index.html", html)

# ---------------------------------------------------------------- recetas
root = "../"
canonical = SITE + "/recetas-bubble-tea/"
crumbs = [("recetas-bubble-tea/", "Recetas de bubble tea")]
cards = ""
recipe_imgs = {"bubble-tea-de-taro": "polvo-taro-bubble-tea", "brown-sugar-milk-tea": "polvo-okinawa-brown-sugar",
               "matcha-latte-frio": "polvo-matcha-taiwan", "soda-italiana-con-sirope": "siropes-de-fruta-linea"}
for r in RECIPES:
    img = recipe_imgs[r["slug"]]
    cards += f"""<article class="card">
  <a class="card-img" href="{root}recetas-bubble-tea/{r['slug']}/" aria-hidden="true" tabindex="-1"><img src="{root}assets/img/{img}-card.webp" alt="" loading="lazy"></a>
  <div class="card-body">
    <h3><a href="{root}recetas-bubble-tea/{r['slug']}/">{r['title']}</a></h3>
    <p class="meta">{r['intro'][:110]}…</p>
    <div class="card-actions"><a class="btn btn-gold" href="{root}recetas-bubble-tea/{r['slug']}/">Ver receta</a></div>
  </div>
</article>"""
html = head(
    "Recetas de Bubble Tea para tu negocio | Insumos Pop",
    "Recetas base de bubble tea para cafeterías y negocios: taro, brown sugar estilo tigre, matcha latte frío y sodas con sirope de fruta. Paso a paso con insumos premium.",
    canonical, root, jsonld=[breadcrumb_ld(crumbs)],
)
html += header_html(root, "recetas")
html += breadcrumb(root, crumbs)
html += f"""
<section class="wrap" style="padding-top:26px">
  <p class="eyebrow">Aprende y vende</p>
  <h1>Recetas de bubble tea</h1>
  <hr class="rule">
  <p style="max-width:46em">Recetas base para arrancar tu menú con nuestros insumos. Las cantidades son sugeridas: ajústalas a tu vaso, tu costo por bebida y el gusto de tus clientes. ¿Necesitas dosificación exacta por producto? <a href="{WA_GENERIC}" target="_blank" rel="noopener">Pídenos la ficha técnica por WhatsApp</a>.</p>
  <div class="grid" style="margin-top:26px;grid-template-columns:repeat(auto-fill,minmax(260px,1fr))">{cards}</div>
</section>
"""
html += footer_html(root)
write_page("recetas-bubble-tea/index.html", html)

for r in RECIPES:
    root = "../../"
    url_rel = "recetas-bubble-tea/" + r["slug"] + "/"
    canonical = SITE + "/" + url_rel
    crumbs = [("recetas-bubble-tea/", "Recetas"), (url_rel, r["title"])]
    img = recipe_imgs[r["slug"]]
    ing = "".join(f"<li>{i}</li>" for i in r["ingredients"])
    steps = "".join(f"<li>{s}</li>" for s in r["steps"])
    prods = ""
    for s in r["uses"]:
        if s in ALL_PRODUCTS:
            p = ALL_PRODUCTS[s]
            prods += f'<li><a href="{root}{product_url(s)}">{p["name"]}</a> — {fmt_cop(p["price"])} · {p["format"]}</li>'
    html = head(
        f"{r['title']} | Receta para negocios | Insumos Pop",
        r["metadesc"], canonical, root,
        jsonld=[breadcrumb_ld(crumbs)],
        og_img=SITE + "/assets/img/" + img + ".webp",
    )
    html += header_html(root, "recetas")
    html += breadcrumb(root, crumbs)
    html += f"""
<section class="wrap" style="padding-top:26px">
  <div class="split" style="align-items:start">
    <div>
      <p class="eyebrow">Receta sugerida</p>
      <h1>{r['title']}</h1>
      <hr class="rule">
      <p>{r['intro']}</p>
      <h2>Ingredientes</h2>
      <ul class="list">{ing}</ul>
      <h2>Preparación</h2>
      <ol class="steps">{steps}</ol>
      <div class="panel"><strong class="gold">Tip de barra:</strong> {r['tip']}</div>
      <h2 style="margin-top:28px">Insumos usados en esta receta</h2>
      <ul class="list">{prods}</ul>
      <div class="cta-row">
        <a class="btn btn-wa" href="{WA_GENERIC}" target="_blank" rel="noopener">{WA_ICON} Cotizar estos insumos</a>
      </div>
    </div>
    <div><img src="{root}assets/img/{img}.webp" alt="" style="border-radius:14px;border:1px solid var(--line)"></div>
  </div>
</section>
"""
    html += footer_html(root)
    write_page(url_rel + "index.html", html)

# ---------------------------------------------------------------- guía emprender
root = "../"
canonical = SITE + "/guia-emprender-bubble-tea/"
crumbs = [("guia-emprender-bubble-tea/", "Guía para emprender con bubble tea")]
html = head(
    "Cómo emprender con Bubble Tea en Colombia | Guía + proveedor | Insumos Pop",
    "Guía práctica para montar bubble tea en tu cafetería o negocio en Colombia: insumos básicos, cómo armar el menú inicial y cómo cotizar con un proveedor de importación directa.",
    canonical, root, jsonld=[breadcrumb_ld(crumbs)],
)
html += header_html(root, "guia")
html += breadcrumb(root, crumbs)
html += f"""
<section class="wrap" style="padding-top:26px;max-width:900px">
  <p class="eyebrow">Guía B2B</p>
  <h1>Cómo emprender con bubble tea en Colombia</h1>
  <hr class="rule">
  <p>El bubble tea pasó de moda pasajera a categoría estable: es visual, rentable por vaso y perfecto para redes sociales. La buena noticia es que no necesitas montar una tienda exclusiva de bubble tea para aprovecharlo — cafeterías, heladerías, reposterías y restaurantes lo están sumando a su carta como línea adicional.</p>

  <h2>1. Lo que necesitas para empezar</h2>
  <p>Con un menú corto y bien elegido puedes arrancar sin sobre-invertir:</p>
  <ul class="list">
    <li><strong>2 o 3 polvos base:</strong> un clásico visual (<a href="{root}polvos-bubble-tea/polvo-taro/">Taro</a>), un lácteo familiar (<a href="{root}polvos-bubble-tea/polvo-hokkaido-milk-tea/">Hokkaido Milk Tea</a>) y una tendencia (<a href="{root}polvos-bubble-tea/polvo-matcha-taiwan/">Matcha</a> u <a href="{root}polvos-bubble-tea/polvo-hojicha/">Hojicha</a>).</li>
    <li><strong>1 o 2 siropes de fruta</strong> para limonadas, sodas italianas y tés fríos: <a href="{root}siropes-bubble-tea/siropes-de-fruta/">12 sabores disponibles</a>.</li>
    <li><strong>Un diferenciador:</strong> <a href="{root}polvos-bubble-tea/polvo-cheese-foam/">Cheese Foam</a> o el efecto tigre con <a href="{root}polvos-bubble-tea/polvo-okinawa-brown-sugar/">Okinawa Brown Sugar</a> te permiten cobrar más por vaso.</li>
    <li><strong>Básicos de barra:</strong> té preparado, leche, hielo, perlas de tapioca, vasos con tapa de cúpula y pitillos gruesos.</li>
  </ul>

  <h2>2. Arma un menú corto que rote</h2>
  <p>Es mejor vender 6 bebidas excelentes que 20 regulares. Una estructura probada: dos milk teas (uno clásico y uno visual), una bebida de matcha o hojicha, dos bebidas frutales con sirope y un especial de temporada. En nuestras <a href="{root}recetas-bubble-tea/">recetas base</a> tienes el paso a paso de cada estilo.</p>

  <h2>3. Cuida el costo por vaso</h2>
  <p>Los polvos y siropes concentrados te permiten estandarizar: define la dosis por bebida, pésala y calcula tu costo real por vaso antes de fijar el precio de carta. Escríbenos y te ayudamos a calcular la dosificación según tu vaso y tu receta.</p>

  <h2>4. Hazlo visible</h2>
  <p>El bubble tea se vende por los ojos: el violeta del taro, las vetas del tiger sugar, el degradé del matcha o el azul del <a href="{root}polvos-bubble-tea/polvo-coral-azul/">Coral Azul</a>. Diseña tus bebidas para la cámara y deja que tus clientes hagan el marketing.</p>

  <h2>5. Según tu negocio</h2>
  <p>Preparamos una página con la selección, el kit y las respuestas específicas de cada tipo de negocio:</p>
  <ul class="list">
    <li><strong>Cafetería de especialidad:</strong> matcha de origen, hojicha y cheese foam. <a href="{root}bubble-tea-para-cafeterias/">Mira los insumos para cafeterías →</a></li>
    <li><strong>Tienda de bubble tea:</strong> los polvos originales de Taiwán con precio de importador. <a href="{root}proveedor-bubble-tea/">Mira el proveedor para tiendas de bubble tea →</a></li>
    <li><strong>Bar o coctelería:</strong> siropes concentrados con costo por copa calculable. <a href="{root}siropes-para-cocteleria/">Mira los siropes para coctelería →</a></li>
    <li><strong>Primer negocio:</strong> kit inicial, recetas y asesoría para arrancar sin adivinar. <a href="{root}kit-emprendedor-bubble-tea/">Mira el kit para emprendedores →</a></li>
    <li><strong>Heladería o repostería:</strong> <a href="{root}polvos-bubble-tea/polvo-taro/">Taro</a>, <a href="{root}polvos-bubble-tea/polvo-mango-coco-hong-kong/">Mango Coconut</a> y <a href="{root}polvos-bubble-tea/polvos-de-fruta/">polvos de fruta</a> para frappés, helados y postres.</li>
  </ul>

  <h2>6. Elige bien a tu proveedor</h2>
  <p>La diferencia entre un bubble tea memorable y uno del montón está en el insumo. En Insumos Pop importamos directo de Taiwán, sin intermediarios: sabores originales de Asia con precio de importador, factura y asesoría real por WhatsApp.</p>

  <div class="panel center" style="margin-top:30px">
    <h2>¿Montamos tu menú juntos?</h2>
    <p class="muted">Cuéntanos qué tipo de negocio tienes y te recomendamos el kit inicial ideal — y si quieres, te enviamos una muestra gratis.</p>
    <a class="btn btn-wa" href="{wa_link('Hola Insumos Pop 👋 Quiero emprender con bubble tea. Mi negocio es: ')}" target="_blank" rel="noopener">{WA_ICON} Hablar con un asesor</a>
  </div>
</section>
"""
html += footer_html(root)
write_page("guia-emprender-bubble-tea/index.html", html)

# ---------------------------------------------------------------- nosotros
canonical = SITE + "/nosotros/"
crumbs = [("nosotros/", "Nosotros")]
html = head(
    "Nosotros | Importador directo de insumos asiáticos | Insumos Pop",
    "Insumos Pop importa directo de Taiwán los sabores premium de Asia para cafeterías, restaurantes y tiendas de bubble tea en Colombia. Sin intermediarios, de la fábrica a tu local.",
    canonical, root, jsonld=[breadcrumb_ld(crumbs)],
)
html += header_html(root, "nosotros")
html += breadcrumb(root, crumbs)
html += f"""
<section class="wrap" style="padding-top:26px;max-width:860px">
  <p class="eyebrow">Quiénes somos</p>
  <h1>Lo premium de Asia, directo a tu carta</h1>
  <hr class="rule">
  <p>En Insumos Pop importamos directo de Taiwán los sabores premium de Asia que en Colombia no se conseguían, o se encontraban en réplicas de baja calidad y sobreprecio. Trabajamos sin intermediarios, de la fábrica a tu local, para que cafeterías de especialidad, restaurantes, heladerías, reposterías y tiendas de bubble tea puedan ofrecer sabores que nadie más tiene: Taro, Hojicha, Matcha, Coral Azul, Mango-Coco de Hong Kong y mucho más, con la máxima calidad de origen y a un precio justo.</p>
  <p class="gold" style="font-style:italic">Más que insumos, te brindamos la diferencia que hace que tu carta destaque y que tus clientes siempre quieran regresar.</p>
  <p>Emitimos factura (Taro Pop S.A.S.) y compartimos ficha técnica y documentación del producto al cotizar. Si quieres probar antes de comprar, pide tu muestra gratis para negocios.</p>
  <div class="benefits" style="margin-top:26px">
    <div class="benefit"><h3>Calidad de origen</h3><p class="muted">Premium taiwanés, no imitaciones.</p></div>
    <div class="benefit"><h3>Precio de importador</h3><p class="muted">Directo de fábrica, sin intermediarios.</p></div>
    <div class="benefit"><h3>Sabores únicos</h3><p class="muted">Lo que tu competencia no tiene.</p></div>
    <div class="benefit"><h3>Asesoría real</h3><p class="muted">Un asesor comercial directo por WhatsApp.</p></div>
  </div>
  <div class="cta-row" style="margin-top:30px">
    <a class="btn btn-wa" href="{WA_GENERIC}" target="_blank" rel="noopener">{WA_ICON} Escríbenos por WhatsApp</a>
    <a class="btn btn-line" href="{root}polvos-bubble-tea/">Ver el catálogo</a>
  </div>
</section>
"""
html += footer_html(root)
write_page("nosotros/index.html", html)

# ---------------------------------------------------------------- envíos y pagos
canonical = SITE + "/envios-y-pagos/"
crumbs = [("envios-y-pagos/", "Envíos y pagos")]
html = head(
    "Envíos y pagos | Insumos Pop",
    "Cómo comprar insumos de bubble tea en Insumos Pop: cotización por WhatsApp, envíos a tu ciudad en Colombia y facturación como Taro Pop S.A.S.",
    canonical, root, jsonld=[breadcrumb_ld(crumbs)],
)
html += header_html(root, "")
html += breadcrumb(root, crumbs)
html += f"""
<section class="wrap" style="padding-top:26px;max-width:860px">
  <p class="eyebrow">Cómo comprar</p>
  <h1>Envíos y pagos</h1>
  <hr class="rule">
  <h2>Así funciona tu pedido</h2>
  <ol class="steps">
    <li><strong>Arma tu cotización.</strong> Agrega productos desde el catálogo o escríbenos directamente por WhatsApp con lo que necesitas.</li>
    <li><strong>Te confirmamos todo por WhatsApp.</strong> Disponibilidad, valor del envío a tu ciudad, tiempos de entrega y medios de pago, antes de que pagues.</li>
    <li><strong>Despachamos tu pedido.</strong> Coordinamos el envío hasta tu local y te compartimos el seguimiento.</li>
  </ol>
  <h2>Cobertura</h2>
  <p>Atendemos negocios en toda Colombia. El valor y el tiempo del envío dependen de tu ciudad y del tamaño del pedido: te los confirmamos en la cotización, sin sorpresas.</p>
  <h2>Precios y facturación</h2>
  <p>Todos los precios del catálogo incluyen IVA. Emitimos factura: operamos bajo la razón social Taro Pop S.A.S. La ficha técnica y la documentación del producto están disponibles al cotizar.</p>
  <h2>¿Dudas?</h2>
  <p>Escríbenos al WhatsApp {WA_DISPLAY} y un asesor comercial te responde directamente.</p>
  <a class="btn btn-wa" href="{wa_link('Hola Insumos Pop 👋 Quiero confirmar el costo y tiempo de envío a mi ciudad: ')}" target="_blank" rel="noopener">{WA_ICON} Confirmar envío a mi ciudad</a>
</section>
"""
html += footer_html(root)
write_page("envios-y-pagos/index.html", html)

# ---------------------------------------------------------------- FAQ
canonical = SITE + "/preguntas-frecuentes/"
crumbs = [("preguntas-frecuentes/", "Preguntas frecuentes")]
faqs = [
    ("¿Venden solo a negocios o también al detal?",
     "Nuestro foco son los negocios: cafeterías, restaurantes, heladerías, reposterías, tiendas de bubble tea y emprendimientos. Si tienes un proyecto en marcha, escríbenos y lo cotizamos."),
    ("¿Los precios incluyen IVA?",
     "Sí. Todos los precios publicados en el catálogo incluyen IVA."),
    ("¿Hacen envíos a toda Colombia?",
     "Sí, coordinamos envíos a las principales ciudades del país. El valor y tiempo de entrega se confirman en tu cotización según tu ciudad y el tamaño del pedido."),
    ("¿Puedo pedir una muestra?",
     "Escríbenos por WhatsApp: contamos con muestras gratis para negocios que quieren probar la calidad antes de su primer pedido."),
    ("¿Cómo hago un pedido?",
     "Agrega productos a tu cotización en la web y envíala por WhatsApp, o escríbenos directamente al " + WA_DISPLAY + ". Un asesor confirma disponibilidad, envío y pago."),
    ("¿De dónde vienen los productos?",
     "Importamos directo de Taiwán, sin intermediarios. Algunas referencias, como el Shizuoka Matcha y el Pure Hojicha, son single origin de Japón."),
    ("¿Tienen dosis y rendimiento por producto?",
     "Sí: la dosificación depende de tu receta y tamaño de vaso, por eso la compartimos junto con la ficha técnica cuando cotizas. Así no te prometemos rendimientos genéricos que no aplican a tu operación."),
    ("¿Emiten factura?",
     "Sí. Operamos bajo la razón social Taro Pop S.A.S. y emitimos factura para tu negocio."),
    ("¿Qué medios de pago reciben?",
     "Te los confirmamos junto con tu cotización, siempre antes de pagar y por escrito, para que tengas todo claro."),
    ("¿Cuánto dura el producto?",
     "La vida útil viene marcada en cada empaque y te la confirmamos junto con la ficha técnica al cotizar. Como regla general, consérvalo en un lugar fresco y seco, bien cerrado después de abrir."),
]
faq_ld = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
        {"@type": "Question", "name": q,
         "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs
    ],
}
html = head(
    "Preguntas frecuentes | Insumos Pop",
    "Resolvemos las dudas más comunes: pedidos mínimos, envíos en Colombia, muestras gratis, facturación, origen de los productos y cómo cotizar.",
    canonical, root, jsonld=[breadcrumb_ld(crumbs), faq_ld],
)
html += header_html(root, "")
html += breadcrumb(root, crumbs)
html += f"""
<section class="wrap" style="padding-top:26px;max-width:800px">
  <p class="eyebrow">Ayuda</p>
  <h1>Preguntas frecuentes</h1>
  <hr class="rule">
  {faq_html(faqs)}
  <div class="cta-row" style="margin-top:28px">
    <a class="btn btn-wa" href="{WA_GENERIC}" target="_blank" rel="noopener">{WA_ICON} ¿Otra pregunta? Escríbenos</a>
  </div>
</section>
"""
html += footer_html(root)
write_page("preguntas-frecuentes/index.html", html)

# ---------------------------------------------------------------- cotizar
canonical = SITE + "/cotizar/"
crumbs = [("cotizar/", "Cotizar")]
biz_opts = "".join(f"<option>{o}</option>" for o in
    ["", "Cafetería", "Tienda de bubble tea", "Restaurante", "Heladería", "Repostería", "Bar / coctelería", "Emprendimiento nuevo", "Otro"])
html = head(
    "Cotiza insumos de bubble tea para tu negocio | Insumos Pop",
    "Arma tu cotización de polvos y siropes para bubble tea y recíbela por WhatsApp. Atendemos cafeterías, restaurantes y emprendimientos en toda Colombia.",
    canonical, root, jsonld=[breadcrumb_ld(crumbs)],
)
html += header_html(root, "", body_class="p-cotizar")
html += breadcrumb(root, crumbs)
html += f"""
<section class="wrap" style="padding-top:26px;max-width:760px">
  <p class="eyebrow">Cotización</p>
  <h1>Cotizar para mi negocio</h1>
  <hr class="rule">
  <div id="quote-empty" class="panel">
    <p><strong>Aún no has agregado productos.</strong></p>
    <p class="muted">Recorre el catálogo y usa “Agregar a cotización”, o si lo prefieres escríbenos directo por WhatsApp.</p>
    <div class="cta-row">
      <a class="btn btn-gold" href="{root}polvos-bubble-tea/">Ver polvos</a>
      <a class="btn btn-line" href="{root}siropes-bubble-tea/">Ver siropes</a>
      <a class="btn btn-wa" href="{WA_GENERIC}" target="_blank" rel="noopener">{WA_ICON} WhatsApp directo</a>
    </div>
  </div>
  <div id="quote-list" aria-live="polite"></div>
  <div id="quote-form-box" style="display:none">
    <p id="quote-total" class="price" style="font-size:1.15rem;margin-top:16px"></p>
    <p id="quote-flavor-hint" class="muted" style="display:none;font-size:.92rem">🍑 Tu cotización incluye siropes o polvos de fruta: recuerda indicar los sabores en las notas.</p>
    <p class="muted" style="font-size:.9rem">El total es una referencia con IVA incluido; el valor del envío se confirma con tu asesor según tu ciudad.</p>
    <form id="quote-form" novalidate>
    <h2 style="margin-top:20px">Tus datos</h2>
    <div class="field"><label for="f-ciudad">Ciudad *</label><input id="f-ciudad" autocomplete="address-level2" required>
      <p class="error" id="e-ciudad">Indica tu ciudad para calcular el envío.</p></div>
    <div class="field"><label for="f-nombre">Nombre (opcional)</label><input id="f-nombre" autocomplete="name"></div>
    <div class="field"><label for="f-negocio">Tipo de negocio</label><select id="f-negocio">{biz_opts}</select></div>
    <div class="field"><label for="f-notas">Notas (opcional)</label><textarea id="f-notas" rows="3" placeholder="Sabores, cantidades especiales, fecha en que lo necesitas…"></textarea></div>
    <div class="cta-row">
      <button class="btn btn-wa" id="quote-send" type="submit">{WA_ICON} Enviar cotización por WhatsApp</button>
    </div>
    </form>
    <p class="muted" style="font-size:.9rem;margin-top:14px">Al enviar se abrirá WhatsApp con tu cotización lista para {WA_DISPLAY}. No guardamos tus datos en ningún servidor.</p>
    <p style="margin-top:10px"><button class="link-clear" id="quote-clear" type="button">Vaciar cotización</button></p>
  </div>
</section>
"""
html += footer_html(root)
write_page("cotizar/index.html", html)

# ---------------------------------------------------------------- home
root = "./"
canonical = SITE + "/"
org_ld = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "Insumos Pop",
    "legalName": "Taro Pop S.A.S.",
    "url": SITE + "/",
    "logo": SITE + "/assets/img/polvo-taro-bubble-tea-card.webp",
    "description": "Importador directo de insumos premium de bubble tea desde Taiwán para negocios en Colombia.",
    "areaServed": "CO",
    "contactPoint": {"@type": "ContactPoint", "contactType": "sales",
                     "telephone": "+57-301-8656016", "availableLanguage": "es"},
}
feat = [ALL_PRODUCTS[s] for s in ["polvo-taro", "polvo-okinawa-brown-sugar", "polvo-matcha-taiwan",
                                  "polvo-coral-azul", "polvo-cheese-foam", "polvo-hojicha"]]
feat_cards = "".join(card(p, root) for p in feat)

HOME_KIT1 = dict(name="Kit Primer Menú",
    pitch="Los 3 polvos con los que arranca un menú que rota, más 2 siropes para limonadas y sodas. Con esto montas 6 bebidas de carta.",
    items=[("polvo-taro", 1, None), ("polvo-hokkaido-milk-tea", 1, None),
           ("polvo-matcha-taiwan", 1, None), ("siropes-de-fruta", 2, " — sabores a elección")])
HOME_KIT2 = dict(name="Kit Diferenciador",
    pitch="El topping y el efecto tigre que te dejan cobrar más por vaso: lo que tu competencia no tiene.",
    items=[("polvo-cheese-foam", 1, None), ("polvo-okinawa-brown-sugar", 1, None)])
home_faqs = [
    ("¿Atienden negocios en cualquier ciudad de Colombia?",
     "Sí. Coordinamos el envío a tu ciudad y te confirmamos valor y tiempos en la cotización."),
    ("¿Puedo probar antes de comprar?",
     "Escríbenos por WhatsApp y pregunta por la muestra gratis para negocios."),
    ("¿Los precios incluyen IVA?",
     "Sí, todos los precios publicados incluyen IVA y emitimos factura (Taro Pop S.A.S.)."),
]
html = head(
    "Insumos Pop | Insumos premium de Bubble Tea en Colombia — Polvos y Siropes",
    "Importador directo de Taiwán: polvos de taro, matcha, hojicha, brown sugar y siropes de fruta para cafeterías, restaurantes y tiendas de bubble tea en Colombia. Cotiza por WhatsApp.",
    canonical, root, jsonld=[org_ld],
    preload="./assets/img/polvo-taro-bubble-tea.webp",
)
html += header_html(root, "")
html += f"""
<div class="hero">
  <div class="wrap hero-grid">
    <div>
      <p class="eyebrow">Sabores premium de Asia · Importador directo de Taiwán</p>
      <h1>Insumos de bubble tea para negocios en Colombia</h1>
      <p class="lead">Polvos y siropes originales de Asia — Taro, Matcha, Hojicha, Brown Sugar, Coral Azul y más — de la fábrica a tu local, sin intermediarios. La diferencia que hace que tu carta destaque.</p>
      <div class="cta-row">
        <a class="btn btn-wa" href="{WA_GENERIC}" target="_blank" rel="noopener">{WA_ICON} Cotizar por WhatsApp</a>
        <a class="btn btn-gold" href="{root}polvos-bubble-tea/">Ver polvos</a>
        <a class="btn btn-line" href="{root}siropes-bubble-tea/">Ver siropes</a>
      </div>
      <p class="sample-note">Pide tu <strong>muestra gratis para negocios</strong> por WhatsApp y prueba la calidad antes de tu primer pedido.</p>
      <div class="trust">
        <div><b>Calidad de origen</b>Premium taiwanés, no imitaciones</div>
        <div><b>Precio de importador</b>Directo de fábrica</div>
        <div><b>Sabores únicos</b>Lo que tu competencia no tiene</div>
      </div>
    </div>
    <img src="{root}assets/img/polvo-taro-bubble-tea.webp" alt="Bolsa de polvo de taro premium Insumos Pop de 1 kg junto a un plato con polvo violeta" width="1100" height="1155" fetchpriority="high">
  </div>
</div>

<section class="wrap">
  <p class="eyebrow">Catálogo</p>
  <h2>¿Qué necesita tu barra?</h2>
  <hr class="rule">
  <div class="tiles">
    <a class="tile" href="{root}polvos-bubble-tea/">
      <img src="{root}assets/img/polvo-matcha-taiwan-card.webp" alt="Polvos premium para bubble tea: bolsa de Taiwan Matcha de Insumos Pop" loading="lazy">
      <div class="tile-body"><h3>Polvos para bubble tea</h3><p>Joyas premium de Asia y polvos de fruta: la base de milk teas, frappés y lattes. Desde {fmt_cop(65000)} el kilo.</p><span class="link">Ver los polvos →</span></div>
    </a>
    <a class="tile" href="{root}siropes-bubble-tea/">
      <img src="{root}assets/img/siropes-de-fruta-linea-card.webp" alt="Siropes de fruta concentrados de Insumos Pop en botellas de 1.9 litros" loading="lazy">
      <div class="tile-body"><h3>Siropes de fruta</h3><p>Concentrados taiwaneses en 12 sabores para cócteles, sodas, limonadas y té. Botella 1.9 L, {fmt_cop(110000)}.</p><span class="link">Ver los siropes →</span></div>
    </a>
  </div>
</section>

<section class="wrap">
  <p class="eyebrow">Destacados</p>
  <h2>Los sabores que diferencian tu carta</h2>
  <hr class="rule">
  <div class="grid">{feat_cards}</div>
</section>

<section class="wrap" id="kits">
  <p class="eyebrow">Para empezar sin enredos</p>
  <h2>Kits sugeridos</h2>
  <hr class="rule">
  <p class="muted" style="max-width:44em">Combos armados con el catálogo real para que no tengas que adivinar. Los agregas a tu cotización en un clic y ajustas cantidades o sabores antes de enviar.</p>
  <div class="split" style="margin-top:20px">
    {kit_html(HOME_KIT1, root, "polvo-taro")}
    {kit_html(HOME_KIT2, root, "polvo-cheese-foam")}
  </div>
  <p class="muted" style="margin-top:18px">¿Ya sabes qué negocio tienes? Preparamos una página para cada uno:
    <a href="{root}bubble-tea-para-cafeterias/">Cafeterías</a> ·
    <a href="{root}proveedor-bubble-tea/">Tiendas de bubble tea</a> ·
    <a href="{root}siropes-para-cocteleria/">Bares y coctelería</a> ·
    <a href="{root}kit-emprendedor-bubble-tea/">Tu primer negocio</a>.
  </p>
</section>

<section class="wrap">
  <div class="split">
    <div class="panel">
      <p class="eyebrow">Empieza tu menú</p>
      <h2>¿Primera vez con bubble tea?</h2>
      <p class="muted">Te contamos qué insumos necesitas, cómo armar un menú corto que rote y cómo cuidar el costo por vaso.</p>
      <a class="btn btn-gold" href="{root}guia-emprender-bubble-tea/">Leer la guía para emprender</a>
    </div>
    <div class="panel">
      <p class="eyebrow">Aprende y vende</p>
      <h2>Recetas listas para tu barra</h2>
      <p class="muted">Bubble tea de taro, brown sugar estilo tigre, matcha latte frío y sodas italianas con sirope: paso a paso.</p>
      <a class="btn btn-gold" href="{root}recetas-bubble-tea/">Ver las recetas</a>
    </div>
  </div>
</section>

<section class="wrap">
  <p class="eyebrow">Ayuda</p>
  <h2>Preguntas frecuentes</h2>
  <hr class="rule">
  <div style="max-width:760px">{faq_html(home_faqs)}</div>
  <p style="margin-top:16px"><a href="{root}preguntas-frecuentes/">Ver todas las preguntas frecuentes →</a></p>
</section>

<section class="cta-final">
  <div class="wrap center">
    <h2>¿Listo para diferenciar tu carta?</h2>
    <p class="muted" style="max-width:38em;margin:0 auto 8px">Insumos disponibles para despacho a negocios en toda Colombia. Escríbenos hoy y pregunta por tu muestra gratis.</p>
    <hr class="rule">
    <a class="btn btn-wa" href="{WA_GENERIC}" target="_blank" rel="noopener">{WA_ICON} WhatsApp directo: {WA_DISPLAY}</a>
  </div>
</section>
"""
html += footer_html(root)
write_page("index.html", html)

# ---------------------------------------------------------------- 404
html = head("Página no encontrada | Insumos Pop", "La página que buscas no existe.", SITE + "/404.html", "/")
# use absolute root for 404 since it can be served from any path
html = html.replace('href="/assets/styles.css"', 'href="/assets/styles.css"')
html += header_html("/", "")
html += """
<section class="wrap center" style="padding:90px 20px">
  <h1>No encontramos esa página</h1>
  <p class="muted">Puede que el enlace haya cambiado. Estos caminos sí llevan a algún lado:</p>
  <div class="cta-row" style="justify-content:center">
    <a class="btn btn-gold" href="/polvos-bubble-tea/">Ver polvos</a>
    <a class="btn btn-line" href="/siropes-bubble-tea/">Ver siropes</a>
    <a class="btn btn-line" href="/">Ir al inicio</a>
  </div>
</section>
"""
html += footer_html("/")
write_page("404.html", html)

# ---------------------------------------------------------------- sitemap + robots
urls = ["", "polvos-bubble-tea/", "siropes-bubble-tea/", "recetas-bubble-tea/",
        "guia-emprender-bubble-tea/", "nosotros/", "envios-y-pagos/",
        "preguntas-frecuentes/", "cotizar/"]
urls += [product_url(p["slug"]) for p in POWDERS]
urls += [product_url(FRUIT_POWDER["slug"]), product_url(SYRUP["slug"])]
urls += ["recetas-bubble-tea/" + r["slug"] + "/" for r in RECIPES]
urls += [pr["slug"] + "/" for pr in PROFILES]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for u in urls:
    sm += f"  <url><loc>{SITE}/{u}</loc><lastmod>{TODAY}</lastmod></url>\n"
sm += "</urlset>\n"
write_page("sitemap.xml", sm)
write_page("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")

# GitHub Pages: dominio personalizado + desactivar Jekyll
write_page("CNAME", DOMAIN + "\n")
write_page(".nojekyll", "")

print(f"OK — {len(urls) + 1} páginas generadas para {SITE}")

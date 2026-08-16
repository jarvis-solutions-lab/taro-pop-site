# -*- coding: utf-8 -*-
"""Generador del sitio estático Insumos Pop."""
import html as html_mod
import json, os, shutil, urllib.parse
from data import WA, WA_DISPLAY, SITE, DOMAIN, POWDERS, FRUIT_POWDER, SYRUP, RECIPES, PROFILES

RAIZ = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(RAIZ, "site")


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

# Navegadores y rastreadores también buscan /favicon.ico directamente.
favicon_src = os.path.join(OUT, "assets", "favicon.ico")
if os.path.isfile(favicon_src):
    shutil.copy2(favicon_src, os.path.join(OUT, "favicon.ico"))

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
<link rel="icon" href="{root}favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="48x48" href="{root}assets/img/favicon-48.png">
<link rel="icon" type="image/png" sizes="192x192" href="{root}assets/img/favicon-192.png">
<link rel="apple-touch-icon" sizes="180x180" href="{root}assets/img/apple-touch-icon.png">
<link rel="manifest" href="{root}site.webmanifest">
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
      <p class="muted">Polvos y siropes para cafeterías, bares y tiendas de bubble tea en Colombia. Precios con IVA, factura y asesoría por WhatsApp.</p>
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
            # El catálogo publicado representa referencias disponibles; actualizar
            # este valor antes de publicar si una referencia deja de estarlo.
            "availability": "https://schema.org/InStock",
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
    seo_name = p.get("seo_name", p["name"])
    html = head(
        f"{seo_name} · {p['format']} | Insumos Pop",
        f"{seo_name} para {p['uses'][0].lower()} y {p['uses'][1].lower()}. {p['format']}, {fmt_cop(p['price'])} con IVA. Consulta ficha técnica y envío en Colombia.",
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
      <a class="btn btn-wa pdp-quick-cta" href="{wa_msg}" target="_blank" rel="noopener">{WA_ICON} Cotizar ahora</a>
      <div class="cond">IVA incluido · Confirma disponibilidad y envío por WhatsApp</div>
      <div class="cond"><strong class="gold">Muestra para negocios:</strong> consulta condiciones antes del primer pedido.</div>
    </div>
    {flavor_select}
    <div class="cta-row">
      <a class="btn btn-wa pdp-main-cta" href="{wa_msg}" target="_blank" rel="noopener">{WA_ICON} Cotizar por WhatsApp</a>
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
    "Polvos para Bubble Tea en Colombia | Insumos Pop",
    "Polvos para bubble tea: taro, matcha, hojicha, brown sugar, milk tea, cheese foam y frutas. Precios con IVA para negocios en Colombia.",
    canonical, root, jsonld=[breadcrumb_ld(crumbs)],
)
html += header_html(root, "polvos")
html += breadcrumb(root, crumbs)
html += f"""
<section class="wrap" style="padding-top:26px">
  <p class="eyebrow">Catálogo</p>
  <h1>Polvos para bubble tea</h1>
  <hr class="rule">
  <p style="max-width:46em">Mezclas para preparar milk tea, frappés y lattes, además de matcha y hojicha puros para cartas de especialidad. Compara presentación, origen, aplicaciones y precio antes de cotizar.</p>
  <p class="muted" style="max-width:46em">Los precios incluyen IVA. Si estás armando una carta nueva, revisa la <a href="{root}guia-emprender-bubble-tea/">guía para empezar</a> o <a href="{WA_GENERIC}" target="_blank" rel="noopener">pide una recomendación por WhatsApp</a>.</p>
  <h2 style="margin-top:34px">Milk tea, matcha, hojicha y toppings <span class="muted" style="font-weight:500;font-size:1rem">· mezclas listas y puros</span></h2>
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
    "Siropes para Bebidas y Coctelería | Insumos Pop",
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
  <p style="max-width:46em">Concentrados de fruta de Taiwán para cócteles, mocktails, frappés, limonadas, sodas italianas y tés fríos. La botella de 1,9 L cuesta $110.000 con IVA incluido.</p>
  <p style="max-width:46em">Define la dosis por bebida para estandarizar sabor y costo. Como referencia matemática, una dosis de 20 ml representa cerca de $1.158 de sirope y una botella alcanza para 95 preparaciones.</p>
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
    "Recetas base de bubble tea para negocios: taro, brown sugar estilo tigre, matcha latte frío y sodas con sirope. Ingredientes y preparación paso a paso.",
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
        f"{r['title']} | Receta | Insumos Pop",
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
    "Cómo Emprender con Bubble Tea en Colombia | Insumos Pop",
    "Guía para montar un menú de bubble tea en Colombia: insumos básicos, recetas, costo por vaso y cómo elegir un proveedor para tu negocio.",
    canonical, root, jsonld=[breadcrumb_ld(crumbs)],
)
html += header_html(root, "guia")
html += breadcrumb(root, crumbs)
html += f"""
<section class="wrap" style="padding-top:26px;max-width:900px">
  <p class="eyebrow">Guía B2B</p>
  <h1>Cómo emprender con bubble tea en Colombia</h1>
  <hr class="rule">
  <p>Puedes incorporar bubble tea y bebidas asiáticas sin convertir todo tu negocio en una tienda especializada. Esta guía te ayuda a elegir un menú corto, estandarizar recetas y calcular el costo del insumo por vaso antes de comprar.</p>

  <h2>1. Lo que necesitas para empezar</h2>
  <p>Con un menú corto y bien elegido puedes arrancar sin sobre-invertir:</p>
  <ul class="list">
    <li><strong>2 o 3 polvos base:</strong> una opción visual (<a href="{root}polvos-bubble-tea/polvo-taro/">Taro</a>), una de perfil lácteo (<a href="{root}polvos-bubble-tea/polvo-hokkaido-milk-tea/">Hokkaido Milk Tea</a>) y una de té (<a href="{root}polvos-bubble-tea/polvo-matcha-taiwan/">Matcha</a> u <a href="{root}polvos-bubble-tea/polvo-hojicha/">Hojicha</a>).</li>
    <li><strong>1 o 2 siropes de fruta</strong> para limonadas, sodas italianas y tés fríos: <a href="{root}siropes-bubble-tea/siropes-de-fruta/">12 sabores disponibles</a>.</li>
    <li><strong>Un producto adicional:</strong> <a href="{root}polvos-bubble-tea/polvo-cheese-foam/">Cheese Foam</a> o el efecto tigre con <a href="{root}polvos-bubble-tea/polvo-okinawa-brown-sugar/">Okinawa Brown Sugar</a> amplían las opciones de la carta.</li>
    <li><strong>Básicos de barra:</strong> té preparado, leche, hielo, perlas de tapioca, vasos con tapa de cúpula y pitillos gruesos.</li>
  </ul>

  <h2>2. Arma un menú corto que rote</h2>
  <p>Un menú corto facilita la capacitación, el inventario y la consistencia. Como punto de partida: dos milk teas, una bebida de matcha o hojicha, dos bebidas frutales y un especial. En nuestras <a href="{root}recetas-bubble-tea/">recetas base</a> tienes el paso a paso de cada estilo.</p>

  <h2>3. Cuida el costo por vaso</h2>
  <p>Los polvos y siropes concentrados te permiten estandarizar: define la dosis por bebida, pésala y calcula tu costo real por vaso antes de fijar el precio de carta. Escríbenos y te ayudamos a calcular la dosificación según tu vaso y tu receta.</p>

  <h2>4. Hazlo visible</h2>
  <p>El color y la presentación influyen en la elección: el violeta del taro, las vetas del brown sugar, el degradé del matcha o el azul del <a href="{root}polvos-bubble-tea/polvo-coral-azul/">Coral Azul</a>. Define una receta que tu equipo pueda repetir antes de pensar en la foto.</p>

  <h2>5. Según tu negocio</h2>
  <p>Preparamos una página con la selección, el kit y las respuestas específicas de cada tipo de negocio:</p>
  <ul class="list">
    <li><strong>Cafetería de especialidad:</strong> matcha de origen, hojicha y cheese foam. <a href="{root}bubble-tea-para-cafeterias/">Mira los insumos para cafeterías →</a></li>
    <li><strong>Tienda de bubble tea:</strong> polvos de Taiwán con precio y presentación publicados. <a href="{root}proveedor-bubble-tea/">Mira la selección para tiendas de bubble tea →</a></li>
    <li><strong>Bar o coctelería:</strong> siropes concentrados con costo por copa calculable. <a href="{root}siropes-para-cocteleria/">Mira los siropes para coctelería →</a></li>
    <li><strong>Primer negocio:</strong> kit inicial, recetas y asesoría para arrancar sin adivinar. <a href="{root}kit-emprendedor-bubble-tea/">Mira el kit para emprendedores →</a></li>
    <li><strong>Heladería o repostería:</strong> <a href="{root}polvos-bubble-tea/polvo-taro/">Taro</a>, <a href="{root}polvos-bubble-tea/polvo-mango-coco-hong-kong/">Mango Coconut</a> y <a href="{root}polvos-bubble-tea/polvos-de-fruta/">polvos de fruta</a> para frappés, helados y postres.</li>
  </ul>

  <h2>6. Elige bien a tu proveedor</h2>
  <p>Compara al proveedor por información útil: presentación, precio con IVA, origen, ficha técnica, dosificación, disponibilidad y soporte después de la compra. En Insumos Pop publicamos los precios, emitimos factura y confirmamos por WhatsApp la ficha técnica, el envío y las existencias.</p>

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
    "Proveedor de Insumos para Bebidas en Colombia | Insumos Pop",
    "Conoce a Insumos Pop, proveedor de polvos y siropes para cafeterías, bares y tiendas de bubble tea. Precios con IVA, factura y muestras para negocios.",
    canonical, root, jsonld=[breadcrumb_ld(crumbs)],
)
html += header_html(root, "nosotros")
html += breadcrumb(root, crumbs)
html += f"""
<section class="wrap" style="padding-top:26px;max-width:860px">
  <p class="eyebrow">Quiénes somos</p>
  <h1>Proveedor de polvos y siropes para negocios en Colombia</h1>
  <hr class="rule">
  <p>Insumos Pop distribuye polvos para milk tea, matcha, hojicha, cheese foam, polvos de fruta y siropes concentrados para cafeterías, restaurantes, bares y tiendas de bubble tea.</p>
  <p>Publicamos presentación y precio con IVA de cada referencia. Al cotizar confirmamos disponibilidad, envío a tu ciudad y documentación del producto.</p>
  <p>Emitimos factura como Taro Pop S.A.S. y ofrecemos muestras para que los negocios prueben el producto con su propia receta antes del primer pedido.</p>
  <div class="benefits" style="margin-top:26px">
    <div class="benefit"><h3>Información antes de comprar</h3><p class="muted">Formato, precio, origen y usos en cada ficha.</p></div>
    <div class="benefit"><h3>Compra formal</h3><p class="muted">Precios con IVA y factura.</p></div>
    <div class="benefit"><h3>Prueba en tu operación</h3><p class="muted">Muestras disponibles para negocios.</p></div>
    <div class="benefit"><h3>Asesoría por WhatsApp</h3><p class="muted">Disponibilidad, dosificación y envío.</p></div>
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
    "logo": {
        "@type": "ImageObject",
        "url": SITE + "/assets/img/logo-insumos-pop.png",
        "width": 512,
        "height": 512,
    },
    "description": "Proveedor de polvos y siropes para tiendas de bubble tea, cafeterías y bares en Colombia.",
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
    pitch="Dos referencias para sumar cheese foam y bebidas estilo tiger brown sugar a tu carta.",
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
    "Insumos para Bubble Tea y Cafeterías en Colombia | Insumos Pop",
    "Polvos para bubble tea, matcha, hojicha, cheese foam y siropes para cafeterías y bares. Precios con IVA, muestra para negocios y envíos en Colombia.",
    canonical, root, jsonld=[org_ld],
    preload="./assets/img/polvo-taro-bubble-tea.webp",
)
html += header_html(root, "")
html += f"""
<div class="hero">
  <div class="wrap hero-grid">
    <div>
      <p class="eyebrow">Polvos y siropes para negocios HORECA</p>
      <h1>Insumos para bubble tea, cafeterías y bares en Colombia</h1>
      <p class="lead">Compra polvos para milk tea, matcha, hojicha, cheese foam y siropes concentrados de fruta. Precios publicados con IVA y asesoría para elegir según tu carta.</p>
      <div class="cta-row">
        <a class="btn btn-wa" href="{wa_link('Hola Insumos Pop 👋 Quiero cotizar insumos para mi negocio. Mi tipo de negocio es: ')}" target="_blank" rel="noopener">{WA_ICON} Cotizar para mi negocio</a>
        <a class="btn btn-line" href="#catalogo">Ver catálogo y precios</a>
      </div>
      <p class="sample-note"><strong>Muestra gratis para negocios:</strong> prueba el producto con tu receta antes del primer pedido.</p>
      <div class="trust">
        <div><b>Precios claros</b>IVA incluido y factura</div>
        <div><b>Compra con menos riesgo</b>Muestra para negocios</div>
        <div><b>Envíos en Colombia</b>Costo y plazo al cotizar</div>
      </div>
    </div>
    <img src="{root}assets/img/polvo-taro-bubble-tea.webp" alt="Bolsa de polvo de taro Insumos Pop de 1 kg junto a un plato con polvo violeta" width="1100" height="1155" fetchpriority="high">
  </div>
</div>

<section class="wrap audience-section">
  <p class="eyebrow">Elige según tu operación</p>
  <h2>¿Qué tipo de negocio tienes?</h2>
  <hr class="rule">
  <div class="audience-grid">
    <a class="audience-card" href="{root}proveedor-bubble-tea/"><strong>Tienda de bubble tea</strong><span>Taro, milk tea, brown sugar y toppings</span></a>
    <a class="audience-card" href="{root}bubble-tea-para-cafeterias/"><strong>Cafetería</strong><span>Matcha, hojicha, frappés y cheese foam</span></a>
    <a class="audience-card" href="{root}siropes-para-cocteleria/"><strong>Bar o restaurante</strong><span>Siropes para cócteles, mocktails y sodas</span></a>
    <a class="audience-card" href="{root}kit-emprendedor-bubble-tea/"><strong>Voy a empezar</strong><span>Kit inicial, recetas y ayuda para costear</span></a>
  </div>
</section>

<section class="wrap" id="catalogo">
  <p class="eyebrow">Catálogo</p>
  <h2>Compra por tipo de insumo</h2>
  <hr class="rule">
  <div class="tiles">
    <a class="tile" href="{root}polvos-bubble-tea/">
      <img src="{root}assets/img/polvo-matcha-taiwan-card.webp" alt="Polvos para bubble tea: bolsa de Taiwan Matcha de Insumos Pop" loading="lazy">
      <div class="tile-body"><h3>Polvos para bubble tea</h3><p>Mezclas para milk tea, frappés y lattes, además de matcha, hojicha y polvos de fruta. Desde {fmt_cop(65000)} el kilo.</p><span class="link">Ver los polvos →</span></div>
    </a>
    <a class="tile" href="{root}siropes-bubble-tea/">
      <img src="{root}assets/img/siropes-de-fruta-linea-card.webp" alt="Siropes de fruta concentrados de Insumos Pop en botellas de 1.9 litros" loading="lazy">
      <div class="tile-body"><h3>Siropes de fruta</h3><p>Concentrados taiwaneses en 12 sabores para cócteles, sodas, limonadas y té. Botella 1.9 L, {fmt_cop(110000)}.</p><span class="link">Ver los siropes →</span></div>
    </a>
  </div>
</section>

<section class="wrap">
  <p class="eyebrow">Destacados</p>
  <h2>Productos más consultados</h2>
  <hr class="rule">
  <div class="grid">{feat_cards}</div>
</section>

<section class="wrap" id="kits">
  <p class="eyebrow">Selecciones para una primera compra</p>
  <h2>Kits sugeridos</h2>
  <hr class="rule">
  <p class="muted" style="max-width:44em">Estos kits agrupan productos del catálogo al mismo precio individual. Puedes ajustar cantidades y sabores antes de enviar la cotización.</p>
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
    <h2>Cotiza con precio, disponibilidad y envío claros</h2>
    <p class="muted" style="max-width:38em;margin:0 auto 8px">Cuéntanos qué negocio tienes y tu ciudad. Te ayudamos a elegir referencias, confirmamos existencias y calculamos el envío antes de que pagues.</p>
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

# ---------------------------------------------------------------- manifest + sitemap + robots
manifest = {
    "name": "Insumos Pop",
    "short_name": "Insumos Pop",
    "start_url": "/",
    "scope": "/",
    "display": "browser",
    "background_color": "#faf7f0",
    "theme_color": "#faf7f0",
    "icons": [
        {"src": "/assets/img/favicon-192.png", "sizes": "192x192", "type": "image/png"},
        {"src": "/assets/img/logo-insumos-pop.png", "sizes": "512x512", "type": "image/png"},
    ],
}
write_page("site.webmanifest", json.dumps(manifest, ensure_ascii=False, separators=(",", ":")))

urls = ["", "polvos-bubble-tea/", "siropes-bubble-tea/", "recetas-bubble-tea/",
        "guia-emprender-bubble-tea/", "nosotros/", "envios-y-pagos/",
        "preguntas-frecuentes/", "cotizar/"]
urls += [product_url(p["slug"]) for p in POWDERS]
urls += [product_url(FRUIT_POWDER["slug"]), product_url(SYRUP["slug"])]
urls += ["recetas-bubble-tea/" + r["slug"] + "/" for r in RECIPES]
urls += [pr["slug"] + "/" for pr in PROFILES]
# Sin <lastmod>: es un catálogo comercial, no un sitio de noticias. Google
# desaconseja fechas de modificación imprecisas, y omitirlas evita que muestre
# "hace X horas" junto al resultado de búsqueda.
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for u in urls:
    sm += f"  <url><loc>{SITE}/{u}</loc></url>\n"
sm += "</urlset>\n"
write_page("sitemap.xml", sm)
write_page("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")

# GitHub Pages: dominio personalizado + desactivar Jekyll
write_page("CNAME", DOMAIN + "\n")
write_page(".nojekyll", "")

print(f"OK — {len(urls) + 1} páginas generadas para {SITE}")

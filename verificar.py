# -*- coding: utf-8 -*-
"""Verifica el sitio generado: enlaces internos, JSON-LD y precios de kits.

Se ejecuta solo en cada publicación (GitHub Actions). Si algo está roto,
la publicación falla y el sitio en vivo NO se rompe.

Uso local:  python3 verificar.py
"""
import html as html_mod
import json
import os
import re
import sys

SITE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")
errores = []
avisos = []

paginas = []
for dp, _, fn in os.walk(SITE_DIR):
    for f in fn:
        if f.endswith(".html"):
            paginas.append(os.path.join(dp, f))

if not paginas:
    print("ERROR: no se encontró ninguna página. ¿Corriste build.py?")
    sys.exit(1)

link_re = re.compile(r'(?:href|src)="([^"]+)"')

for pagina in paginas:
    base = os.path.dirname(pagina)
    rel = os.path.relpath(pagina, SITE_DIR)
    contenido = open(pagina, encoding="utf-8").read()

    # 1. JSON-LD válido
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', contenido, re.S):
        try:
            json.loads(m.group(1))
        except Exception as e:
            errores.append(f"{rel}: JSON-LD inválido ({e})")

    # 2. Los Product con Offer deben declarar disponibilidad para Google.
    for m in re.finditer(r'<script type="application/ld\\+json">(.*?)</script>', contenido, re.S):
        try:
            bloque = json.loads(m.group(1))
        except Exception:
            continue  # El JSON-LD inválido ya se reportó arriba.
        if bloque.get("@type") == "Product" and bloque.get("offers"):
            availability = bloque["offers"].get("availability")
            if not isinstance(availability, str) or not availability.startswith("https://schema.org/"):
                errores.append(f"{rel}: Product.offer sin availability de Schema.org")

    # 3. Enlaces internos que existen
    if rel != "404.html":
        for m in link_re.finditer(contenido):
            url = m.group(1)
            if url.startswith(("http", "mailto:", "tel:", "data:", "#")):
                continue
            destino = os.path.normpath(os.path.join(base, url.split("#")[0]))
            if url.split("#")[0].endswith("/") or os.path.isdir(destino):
                destino = os.path.join(destino, "index.html")
            if not os.path.exists(destino):
                errores.append(f"{rel}: enlace roto → {url}")

    # 4. Cada página con título y descripción únicos y no vacíos
    if not re.search(r"<title>.{15,}</title>", contenido):
        errores.append(f"{rel}: falta <title> o es demasiado corto")
    if not re.search(r'<meta name="description" content=".{50,}"', contenido):
        avisos.append(f"{rel}: meta description corta o ausente")

    # 5. Los precios de los kits deben coincidir con la suma real del catálogo
    mostrados = re.findall(r'class="kit-price">([^<]+)', contenido)
    kits = re.findall(r'data-kit="([^"]+)"', contenido)
    for mostrado, kit in zip(mostrados, kits):
        items = json.loads(html_mod.unescape(kit))
        real = sum(i["price"] * i["qty"] for i in items)
        real_txt = "$" + f"{real:,}".replace(",", ".")
        if real_txt not in mostrado:
            errores.append(f"{rel}: kit muestra {mostrado.strip()} pero suma {real_txt}")

# 6. Títulos duplicados entre páginas (mala señal para Google)
titulos = {}
for pagina in paginas:
    rel = os.path.relpath(pagina, SITE_DIR)
    m = re.search(r"<title>(.*?)</title>", open(pagina, encoding="utf-8").read(), re.S)
    if m:
        titulos.setdefault(m.group(1).strip(), []).append(rel)
for titulo, cuales in titulos.items():
    if len(cuales) > 1:
        errores.append(f"Título duplicado en {len(cuales)} páginas: {', '.join(cuales)}")

# 6. Archivos que GitHub Pages necesita
for necesario in ["CNAME", "sitemap.xml", "robots.txt", "index.html", "favicon.ico", "site.webmanifest"]:
    if not os.path.exists(os.path.join(SITE_DIR, necesario)):
        errores.append(f"Falta el archivo {necesario} en site/")

print(f"Revisadas {len(paginas)} páginas.")
for a in avisos:
    print("  AVISO:", a)
if errores:
    print(f"\n{len(errores)} problema(s) encontrados:")
    for e in errores:
        print("  ✗", e)
    sys.exit(1)
print("Todo correcto: enlaces, JSON-LD, títulos únicos y precios de kits ✔")

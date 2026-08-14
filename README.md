# Insumos Pop — sitio web

Sitio estático (32 páginas) de Insumos Pop: importador directo de insumos premium para bubble tea desde Taiwán, para negocios en Colombia.

**Se publica solo:** cada `git push` a `main` reconstruye el sitio y lo publica. No hay que subir archivos a mano.

---

## Cómo hacer cambios

### Cambiar un precio, agregar un producto o editar un texto

Todo el contenido vive en **`data.py`**. No hay que tocar HTML.

```python
dict(
    slug="polvo-taro",
    name="Polvo de Taro",
    price=95000,          # ← cambias esto
    format="Bolsa 1 kg",
    ...
)
```

Guardas, haces `git commit` y `git push`. En 1–2 minutos el sitio está actualizado: la ficha, las tarjetas del catálogo, el costo por gramo, los precios de los kits que incluyen ese producto y los datos estructurados de Google se recalculan solos.

### Cambiar el número de WhatsApp

Está en dos lugares: `WA` en `data.py` (para todos los enlaces) y `WA_NUMBER` en `site/assets/site.js` (para el cotizador).

### Cambiar el dominio

Ver `DESPLIEGUE.md`. Es una sola variable, no hay que editar código.

---

## Estructura

```
├── data.py                    Todo el contenido: productos, precios, recetas, perfiles
├── build.py                   Genera las 32 páginas HTML desde data.py
├── verificar.py               Revisa enlaces, JSON-LD, precios y títulos antes de publicar
├── site/                      Salida generada localmente (no se versiona)
│   ├── index.html             ...y las demás páginas
│   └── assets/                Copia de los recursos durante el build
├── .github/workflows/         Publicación automática
├── DESPLIEGUE.md              Cómo publicar y cómo migrar el dominio
└── LEEME-PUBLICAR.md          Guía para quien no es técnico
```

**Importante:** `build.py` regenera `site/` completa para publicar, copiando los recursos desde `assets/`. Las imágenes, el CSS y el JS fuente viven en `assets/`; `site/` es una salida local ignorada por Git.

---

## Probarlo en tu computador (opcional)

```bash
python3 build.py                       # genera el sitio
python3 verificar.py                   # revisa que todo esté bien
cd site && python3 -m http.server 8000 # ábrelo en http://localhost:8000
```

Para ver cómo quedaría con otro dominio:

```bash
SITE_URL=https://insumospop.co python3 build.py
```

---

## Qué revisa `verificar.py` antes de publicar

Si algo de esto falla, la publicación se detiene y **el sitio en vivo no se rompe**:

- Ningún enlace interno roto
- JSON-LD (datos estructurados de Google) válido en las 32 páginas
- Títulos únicos por página
- Los precios de los kits coinciden con la suma real del catálogo
- Existen `CNAME`, `sitemap.xml`, `robots.txt` e `index.html`

---

## Qué incluye el sitio

- 14 fichas de producto con precios del catálogo (IVA incluido) y costo por gramo
- 2 categorías: polvos y siropes
- 4 páginas por perfil de cliente (tiendas de bubble tea, cafeterías, emprendedores, bares) con kit propio y WhatsApp segmentado
- 4 recetas paso a paso y guía para emprender
- Cotizador que arma el pedido y lo envía por WhatsApp, sin servidor ni base de datos
- Modo claro y oscuro con preferencia recordada
- SEO: URLs limpias, datos estructurados (Product, FAQ, Organization, ItemList, Breadcrumb), sitemap y robots

Costo de operación: **$0 de hosting**. Solo se paga el dominio.

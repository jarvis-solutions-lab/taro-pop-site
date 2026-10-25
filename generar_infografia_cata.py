# -*- coding: utf-8 -*-
"""Genera las imágenes de la página «Cómo catar tu muestra».

  assets/img/cata-muestra-infografia.png / .webp   1080×1350, para descargar o enviar por WhatsApp
  assets/img/cata-muestra-og.png                   1200×630, vista previa al compartir el enlace

No corre en cada publicación: solo hay que ejecutarlo si cambian los pasos.
Necesita Node con Playwright (Chromium) y Pillow:   python3 generar_infografia_cata.py
"""
import os, subprocess, tempfile
from PIL import Image
from data import CATA, DOMAIN
from ilustraciones_cata import cup_svg, milk_scale_svg

RAIZ = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(RAIZ, "assets", "img")

BASE_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Plus Jakarta Sans',system-ui,sans-serif;color:#1e1a2e;background:#fff}
.brand{font-weight:800;letter-spacing:-.02em}.brand span{color:#6a3fa0}
.eyebrow{color:#6a3fa0;text-transform:uppercase;letter-spacing:.14em;font-weight:800}
h1{font-weight:800;letter-spacing:-.03em;line-height:1.05}
.rule{width:64px;height:6px;border-radius:9px;background:linear-gradient(90deg,#6a3fa0,#7ec891)}
.cups{list-style:none;display:grid;grid-template-columns:repeat(5,1fr)}
.cups li{display:flex;flex-direction:column;align-items:center;text-align:center;position:relative}
.cups li+li::before{content:"→";position:absolute;color:#6a3fa0;font-weight:800}
.n{border-radius:50%;background:#efe6fb;color:#532f80;font-weight:800;display:flex;align-items:center;justify-content:center}
.lbl{font-weight:800;line-height:1.2}
svg{color:#1e1a2e}
"""

FONT = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
        'family=Plus+Jakarta+Sans:wght@500;700;800&display=block">')


def cups(n_size, lbl_size):
    return "".join(f'<li><span class="n" style="width:{n_size}px;height:{n_size}px;font-size:{n_size * .5}px">{n}</span>'
                   f'{cup_svg(n)}<span class="lbl" style="font-size:{lbl_size}px">{l}</span></li>'
                   for n, l in enumerate(CATA["step_labels"], 1))


def infografia():
    escala = "".join(f'<div class="sc">{milk_scale_svg(ml)}<b{" class=on" if ml == 100 else ""}>{ml} ml</b></div>'
                     for ml in range(100, 200, 20))
    return f"""<!doctype html><html><head><meta charset="utf-8">{FONT}<style>{BASE_CSS}
body{{width:1080px;height:1350px;padding:64px 64px 52px;display:flex;flex-direction:column;
  background:radial-gradient(900px 500px at 100% 0,#efe6fb,transparent 70%),radial-gradient(700px 500px at 0 100%,#e6f4e9,transparent 70%),#fff}}
.top{{display:flex;justify-content:space-between;align-items:center}}
.brand{{font-size:34px}} .eyebrow{{font-size:20px}}
h1{{font-size:78px;margin:34px 0 20px}}
.cups{{background:#fff;border:2px solid #ebe7f2;border-radius:32px;padding:36px 22px 30px;margin-top:40px;gap:14px}}
.cups li{{gap:14px}} .cups li+li::before{{left:-16px;top:44%;font-size:30px}}
.cups svg{{width:150px;height:auto}}
.dulce{{margin-top:34px;background:#efe6fb;border-radius:32px;padding:32px 40px}}
.dulce h2{{font-size:42px;letter-spacing:-.02em;margin-bottom:10px}}
.dulce p{{font-size:25px;line-height:1.45;color:#3d3650}}
.punto{{margin-top:30px;display:grid;grid-template-columns:1.05fr 1fr;gap:30px;align-items:center}}
.punto h2{{font-size:36px;letter-spacing:-.02em;margin-bottom:8px}}
.punto p{{font-size:23px;line-height:1.45;color:#3d3650}}
.escala{{display:flex;gap:10px;align-items:flex-end;justify-content:space-between}}
.sc{{display:flex;flex-direction:column;align-items:center;gap:6px}} .sc svg{{width:70px}}
.sc b{{font-size:18px;color:#645e76}} .sc b.on{{color:#532f80}}
.foot{{margin-top:auto;display:flex;justify-content:space-between;align-items:center;font-size:22px;color:#645e76;
  border-top:2px solid #ebe7f2;padding-top:24px}}
.foot strong{{color:#1e1a2e}}
</style></head><body>
<div class="top"><p class="brand">Insumos <span>Pop</span></p><p class="eyebrow">Guía de cata</p></div>
<h1>Cómo catar tu<br>muestra en 5 pasos</h1>
<div class="rule"></div>
<ol class="cups">{cups(44, 23)}</ol>
<div class="dulce"><h2>Va a quedar dulce. Eso es lo que queremos.</h2>
<p>Con 100 ml de leche la mezcla queda concentrada a propósito, para que percibas el sabor completo: el cuerpo, el retrogusto y la textura.</p></div>
<div class="punto">
  <div><h2>Encuentra tu punto</h2><p>Agrega leche de <strong>20 en 20 ml</strong> hasta que te guste. Anota cuánta usaste: <strong>ese número es tu receta ✅</strong></p></div>
  <div class="escala">{escala}</div>
</div>
<div class="foot"><span>Agua a 85 °C, <strong>no hirviendo</strong> ❗</span><span>{DOMAIN}</span></div>
</body></html>"""


def og():
    return f"""<!doctype html><html><head><meta charset="utf-8">{FONT}<style>{BASE_CSS}
body{{width:1200px;height:630px;padding:56px 64px;display:flex;flex-direction:column;
  background:radial-gradient(800px 420px at 100% 0,#efe6fb,transparent 70%),radial-gradient(600px 400px at 0 100%,#e6f4e9,transparent 70%),#fff}}
.brand{{font-size:30px}} .eyebrow{{font-size:18px;margin-top:26px}}
h1{{font-size:64px;margin:12px 0 18px}}
.cups{{margin-top:auto;gap:18px}} .cups li{{gap:10px}}
.cups li+li::before{{left:-18px;top:44%;font-size:28px}} .cups svg{{width:120px;height:auto}}
</style></head><body>
<p class="brand">Insumos <span>Pop</span></p>
<p class="eyebrow">Para quienes recibieron una muestra</p>
<h1>Cómo catar tu muestra</h1>
<div class="rule"></div>
<ol class="cups">{cups(34, 20)}</ol>
</body></html>"""


RENDER_JS = """
const {chromium} = require('playwright');
(async () => {
  const [html, out, w, h] = process.argv.slice(1);
  const b = await chromium.launch();
  const p = await b.newPage({viewport: {width: +w, height: +h}});
  await p.goto('file://' + html, {waitUntil: 'networkidle'});
  await p.evaluate(() => document.fonts.ready);
  await p.screenshot({path: out});
  await b.close();
})();
"""


def render(html, out, w, h):
    with tempfile.TemporaryDirectory() as tmp:
        src = os.path.join(tmp, "pagina.html")
        with open(src, "w", encoding="utf-8") as f:
            f.write(html)
        subprocess.run(["node", "-e", RENDER_JS, src, out, str(w), str(h)], check=True)


png = os.path.join(IMG, "cata-muestra-infografia.png")
render(infografia(), png, 1080, 1350)
Image.open(png).convert("RGB").resize((540, 675), Image.LANCZOS).save(
    os.path.join(IMG, "cata-muestra-infografia.webp"), "WEBP", quality=88)
render(og(), os.path.join(IMG, "cata-muestra-og.png"), 1200, 630)
print("Listo: cata-muestra-infografia.png/.webp y cata-muestra-og.png en assets/img/")

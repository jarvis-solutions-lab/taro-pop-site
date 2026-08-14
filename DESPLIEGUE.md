# Cómo publicar el sitio (y no romper el correo)

Guía escrita para **tu caso concreto**: dominio `taropop.co`, correo en Google Workspace, código en GitHub.

**Costo total: $0 de hosting.** Solo pagas el dominio.

---

## Antes de empezar: cómo está tu dominio hoy

Consulté los registros públicos de `taropop.co` y esto es lo que hay:

| Registro | Valor actual | Qué es | ¿Se toca? |
|---|---|---|---|
| NS | `ns-cloud-d1` a `d4.googledomains.com` | Tu DNS lo administra Google | No |
| **MX** | `1 smtp.google.com` | **Tu correo de Google Workspace** | **NUNCA** |
| **TXT** | `v=spf1 include:_spf.google.com ~all` | SPF: evita que tu correo caiga en spam | **NUNCA** |
| **TXT** | `google._domainkey` (DKIM) | Firma tu correo como auténtico | **NUNCA** |
| A | `198.185.159.144` y 3 más | Tu web actual, apuntando a Squarespace | Sí, estos cambian |
| CNAME | `www` → `ext-sq.squarespace.com` | El www, también a Squarespace | Sí, este cambia |

**La idea clave:** el correo vive en los registros **MX y TXT**; la web vive en los registros **A y CNAME**. Son independientes. Vamos a cambiar solo los de la web. Tu correo no se entera.

> **Ojo con Squarespace:** hoy tu dominio apunta ahí. Si estás pagando un plan mensual de Squarespace (suelen ser US$16–25/mes ≈ US$200–300 al año), al terminar esta guía dejará de usarse y puedes cancelarlo. Revisa tu facturación: es probablemente el mayor ahorro de todo este proceso. **Cancélalo solo después** de que el sitio nuevo esté funcionando.

---

## Por qué GitHub Pages y no Cloudflare

Los dos son gratis. La diferencia está en el riesgo:

- **Cloudflare Pages** exige mover los *nameservers* a Cloudflare para usar un dominio sin www. Eso implica recrear tus registros de correo a mano. Si se hace mal, dejas de recibir emails.
- **GitHub Pages** solo necesita que cambies 4 registros A. **Los MX ni se tocan.** Además tu código ya está en GitHub.

Para un sitio de 2 MB y 32 páginas, GitHub Pages sobra: soporta hasta 1 GB de sitio y ~100 GB de tráfico al mes.

*(Si algún día quieres Cloudflare, la mejor jugada es registrar `insumospop.com` directamente en Cloudflare Registrar —vende a precio de costo, sin margen— porque ese dominio nace sin correo que arriesgar. Está explicado al final.)*

---

## Parte 1 — Publicar el sitio (10 minutos)

### 1. Sube el proyecto completo a tu repositorio

Ya subiste la carpeta `site`. Falta el resto, que es lo que permite la publicación automática:

```
build.py   data.py   verificar.py   README.md   DESPLIEGUE.md   .gitignore   .github/
```

Si usas la web de GitHub, arrastra estos archivos a la raíz del repositorio (no dentro de `site`).

### 2. Activa GitHub Pages

En tu repositorio: **Settings → Pages → Build and deployment → Source: GitHub Actions**.

Eso es todo. No elijas rama ni carpeta: el flujo de trabajo ya está en `.github/workflows/deploy.yml`.

### 3. Verifica la primera publicación

Ve a la pestaña **Actions**. Verás "Publicar sitio" ejecutándose. Tarda ~1 minuto y hace tres cosas: genera las 32 páginas, revisa que no haya enlaces rotos ni precios inconsistentes, y publica.

Cuando termine en verde, tu sitio ya está en línea en `https://<tu-usuario>.github.io/<repositorio>/`. Ábrelo y compruébalo antes de tocar el DNS.

> Si el paso de verificación falla, el sitio anterior sigue intacto. Es a propósito: prefiere no publicar antes que publicar algo roto.

---

## Parte 2 — Conectar taropop.co (5 minutos + espera)

### 1. Dile a GitHub cuál es tu dominio

**Settings → Pages → Custom domain** → escribe `taropop.co` → Save.

(El archivo `CNAME` ya se genera solo con ese valor.)

### 2. Cambia los registros DNS

Entra donde administras el DNS de `taropop.co` (Google Domains/Squarespace, o el panel de Google Cloud DNS).

**Borra** los 4 registros A que apuntan a Squarespace:

```
198.185.159.144    198.185.159.145    198.49.23.144    198.49.23.145
```

**Crea** estos 4 registros A para el dominio raíz (`@` o vacío):

```
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

**Cambia** el CNAME de `www`: de `ext-sq.squarespace.com` a `<tu-usuario>.github.io`

**No toques nada más.** Los MX y los TXT se quedan exactamente como están.

### 3. Espera y activa el candado

El cambio tarda entre 15 minutos y unas horas en propagarse. Cuando `taropop.co` muestre tu sitio nuevo, vuelve a **Settings → Pages** y marca la casilla **Enforce HTTPS**. El certificado es gratis y se renueva solo.

### 4. Comprueba que el correo sigue bien

Mándate un email a tu dirección de `@taropop.co` desde otra cuenta. Debe llegar normal. (No debería fallar: no tocaste los MX.)

---

## Parte 3 — Cuando compres insumospop.com

El sitio ya está preparado: **el dominio es una variable, no está escrito en el código**.

1. Compra el dominio (Cloudflare Registrar, Namecheap o Porkbun; ~US$10–15 al año).
2. En GitHub: **Settings → Secrets and variables → Actions → Variables → New variable**
   - Nombre: `SITE_URL`
   - Valor: `https://insumospop.com`
3. En **Settings → Pages → Custom domain**, escribe `insumospop.com`.
4. En el DNS del dominio nuevo, crea los mismos 4 registros A de GitHub y el CNAME de `www`.
5. Haz cualquier push (o lanza el flujo a mano desde Actions). Las 32 páginas, el `sitemap.xml`, las URLs canónicas y el `CNAME` se regeneran con el dominio nuevo.

**Qué hacer con taropop.co:** déjalo como está para el correo (los MX no dependen de la web) y redirige la web al dominio nuevo. Así no pierdes a nadie que tenga el enlace viejo.

**Importante para Google:** cuando cambies de dominio, avísale en Search Console con la herramienta de "Cambio de dirección". Si no, pierdes el posicionamiento que hayas ganado.

---

## Después de publicar: 4 cosas que valen la pena

1. **Google Search Console** — verifica el dominio y envía `https://taropop.co/sitemap.xml`. Es gratis y es como sabrás qué busca la gente para llegarte.
2. **Perfil de Negocio de Google** — para aparecer en Maps y en búsquedas locales.
3. **Google Analytics** (opcional) — si lo quieres, pásame el ID de medición y lo agrego.
4. **Protege tu correo con DMARC** — hoy tienes SPF y DKIM, pero te falta DMARC. Sin él, cualquiera puede intentar suplantar tu dominio para estafar a tus clientes. Es un solo registro TXT:

   - Nombre: `_dmarc`
   - Valor: `v=DMARC1; p=none; rua=mailto:tu-correo@taropop.co`

   Empieza con `p=none` (solo observa y te reporta). Cuando confirmes que todo tu correo legítimo pasa bien, súbelo a `p=quarantine`.

---

## Resumen de costos al año

| Concepto | Costo |
|---|---|
| Hosting (GitHub Pages) | $0 |
| Certificado HTTPS | $0 |
| Publicación automática | $0 |
| Dominio `.co` (ya lo tienes) | ~US$25–35 |
| Dominio `.com` (si lo compras) | ~US$10–15 |
| **Squarespace, si lo cancelas** | **–US$200 a –US$300** |

---

## Si algo sale mal

- **La publicación falla en Actions** → abre el registro del paso "Verificar": dice exactamente qué enlace o precio está mal.
- **El dominio muestra "404" de GitHub** → revisa que Custom domain esté escrito igual que en el archivo `site/CNAME`.
- **Sale aviso de certificado** → normal las primeras horas; espera a que propague y marca "Enforce HTTPS".
- **Dejó de llegar correo** → significa que se tocaron los MX. Restaura: MX `smtp.google.com` con prioridad `1`, y el TXT `v=spf1 include:_spf.google.com ~all`.

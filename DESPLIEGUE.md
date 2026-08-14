# Publicar Insumos Pop en `insumospop.co`

El sitio se publica en GitHub Pages desde el repositorio `jarvis-solutions-lab/taro-pop-site` mediante GitHub Actions.

## Configuración de producción

- URL canónica: `https://insumospop.co`
- Dominio personalizado de GitHub Pages: `insumospop.co`
- Variable de Actions: `SITE_URL=https://insumospop.co`
- Archivo generado: `site/CNAME` con el valor `insumospop.co`
- Dirección de `www`: `jarvis-solutions-lab.github.io`

Cada `push` a `main` ejecuta `build.py`, valida el resultado con `verificar.py` y publica la carpeta `site/`.

## DNS en Porkbun

En **Domain Management → insumospop.co → DNS**, elimina solamente los registros web de estacionamiento (*parking*) que entren en conflicto:

- Registros `A` para el host raíz (`@` o vacío) que apunten a `207.207.210.229` o `207.207.210.107`.
- El `CNAME` de `www` que apunte a `pixie.porkbun.com`.

Crea estos registros:

| Tipo | Host | Respuesta/valor |
|---|---|---|
| A | `@` (o vacío, según el formulario) | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |
| CNAME | `www` | `jarvis-solutions-lab.github.io` |

Usa el TTL predeterminado. No agregues `https://`, rutas ni el nombre del repositorio en los valores DNS.

**No borres registros MX o TXT** si en el futuro se configura correo, verificación de servicios, SPF, DKIM o DMARC.

## Verificación

Después de guardar los DNS:

```bash
dig +short insumospop.co A
dig +short www.insumospop.co CNAME
```

El dominio raíz debe devolver las cuatro IP de GitHub Pages y `www` debe devolver `jarvis-solutions-lab.github.io.`. La propagación puede tardar desde minutos hasta 48 horas.

En **GitHub → Settings → Pages**, espera a que termine la comprobación DNS y confirma que **Enforce HTTPS** esté habilitado. El certificado TLS puede tardar un poco más que el DNS.

Comprueba finalmente:

- `https://insumospop.co/`
- `https://www.insumospop.co/` (debe redirigir al dominio canónico)
- `https://insumospop.co/sitemap.xml`
- `https://insumospop.co/robots.txt`

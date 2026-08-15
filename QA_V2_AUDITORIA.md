# QA v2: auditoría SEO y conversión

## Veredicto sin maquillaje

La versión anterior tenía buen diseño, precios visibles y un flujo de cotización funcional. El problema estaba en el argumento de venta: repetía "premium", "único", "original" y "lo que tu competencia no tiene", pero mostraba poca evidencia para sostenerlo. Ese lenguaje puede llamar la atención, pero también activa desconfianza en un comprador HORECA que necesita comparar composición, rendimiento, disponibilidad, documentación y costo por bebida.

El sitio tampoco puede prometer el puesto #1 en Google ni una venta "casi garantizada". Nadie controla el ranking, la demanda local o la decisión del comprador. Google recomienda contenido útil y único, escrito para personas, y afirma que esto influye más en la presencia orgánica que la mayoría de ajustes aislados.[1][2] La estrategia correcta es ganar primero las búsquedas específicas que coinciden con el catálogo y construir autoridad con evidencia propia.

## Lo que estaba mal

1. **La portada tardaba en responder "qué venden, para quién y bajo qué condiciones".** En móvil aparecía la foto antes del mensaje y el visitante tenía que inferir si era una tienda al detal o un proveedor B2B.
2. **Había demasiada poesía y poca utilidad operativa.** Frases como "detiene el scroll", "el secreto mejor guardado" o "la próxima gran tendencia" ocupaban el espacio que debería responder dosis, uso, formato y costo.
3. **Varias promesas eran imposibles de demostrar.** "Casi nadie lo ofrece", "se vende solo" o "máxima calidad" no ayudan al SEO ni al cierre si no tienen datos, pruebas o testimonios verificables.
4. **Los títulos de varias páginas eran largos.** Google recomienda títulos descriptivos, concisos y sin texto repetitivo.[3]
5. **Las metadescripciones de producto mezclaban demasiadas afirmaciones.** Google puede usar el contenido visible o la metadescripción para el snippet y recomienda que cada descripción sea específica, útil y única.[4]
6. **La navegación principal no segmentaba rápido al comprador.** Una cafetería, una tienda de bubble tea, un bar y un emprendedor tienen objeciones distintas.
7. **Falta prueba comercial.** No hay testimonios autorizados, casos, fotos de bebidas preparadas por clientes, cifras de recompra ni ciudades atendidas verificadas.
8. **Falta información de compras HORECA.** El usuario todavía debe preguntar por dosis, rendimiento, ingredientes, alérgenos, vida útil, pedido mínimo, escalas de precio, disponibilidad y tiempos de despacho.
9. **El catálogo no cubre toda la intención genérica "insumos para bubble tea".** Otros resultados visibles ofrecen perlas, toppings, kits y/o una oferta integral.[5][6][7] Insumos Pop puede competir mejor primero en consultas donde sí tiene profundidad: polvos, taro, matcha, hojicha, cheese foam y siropes.
10. **No existe medición de conversión.** Sin eventos de analítica no sabemos qué página, producto o CTA produce conversaciones y ventas.

## Hipótesis de conversión aplicada en QA

La primera pantalla ahora sigue esta secuencia:

1. **Relevancia:** "Insumos para bubble tea, cafeterías y bares en Colombia".
2. **Oferta concreta:** polvos, matcha, hojicha, cheese foam y siropes.
3. **Reducción de riesgo:** precios con IVA, factura, muestra y confirmación del envío.
4. **Acción principal:** cotizar para el negocio.
5. **Alternativa sin compromiso:** ver catálogo y precios.

Después del hero, el visitante elige su tipo de negocio. Esto reduce la carga de buscar entre productos y lo envía a una landing con lenguaje, kit, objeciones y CTA específicos.

## Cambios implementados en esta rama QA

- Nueva propuesta de valor y metadatos de portada.
- Texto antes de la fotografía en móvil.
- Un CTA comercial principal y un CTA informativo secundario.
- Señales de confianza concretas: IVA/factura, muestra y envío.
- Selector inmediato para tienda de bubble tea, cafetería, bar/restaurante o negocio nuevo.
- Reescritura de las categorías de polvos y siropes.
- Reescritura de las cuatro landings por tipo de cliente.
- Reescritura de teasers y descripciones de todo el catálogo.
- Eliminación de afirmaciones vagas, absolutas o no demostradas.
- Títulos y metadescripciones más concisos y alineados con cada intención.
- CTA explícito junto al precio en fichas de producto móviles, sin duplicarlo en escritorio.
- Reescritura de la guía para priorizar estandarización, inventario y costo por vaso.
- Página "Nosotros" centrada en hechos verificables del proceso de compra.

## Mapa SEO recomendado

| Intención | Página objetivo | Papel en el embudo |
|---|---|---|
| insumos para bubble tea Colombia | `/` y `/proveedor-bubble-tea/` | Descubrimiento B2B |
| proveedor de bubble tea Colombia | `/proveedor-bubble-tea/` | Evaluación de proveedor |
| polvos para bubble tea | `/polvos-bubble-tea/` | Comparación de categoría |
| polvo de taro Colombia | `/polvos-bubble-tea/polvo-taro/` | Compra de referencia |
| matcha para cafeterías | `/bubble-tea-para-cafeterias/` | Solución por negocio |
| hojicha Colombia | fichas de Hojicha y Pure Hojicha | Compra de referencia |
| siropes para coctelería | `/siropes-para-cocteleria/` | Solución por negocio |
| siropes de fruta para bebidas | `/siropes-bubble-tea/` | Comparación de categoría |
| kit para empezar bubble tea | `/kit-emprendedor-bubble-tea/` | Compra asistida |
| recetas de bubble tea para negocio | `/recetas-bubble-tea/` | Autoridad y consideración |

## Información que falta para convertir mejor

No debe publicarse nada de lo siguiente hasta tener datos reales:

1. Pedido mínimo por referencia y por envío.
2. Escalas de precio por volumen.
3. Inventario y tiempos normales de reposición.
4. Condiciones exactas de la muestra: tamaño, cobertura de envío y quién califica.
5. Ingredientes, alérgenos y tabla nutricional de cada referencia.
6. Vida útil cerrada y después de abrir.
7. Registros, permisos o certificaciones aplicables.
8. Dosificación oficial y rendimiento por producto.
9. Ciudades atendidas, transportadoras y rangos reales de entrega.
10. Medios de pago.
11. Testimonios con autorización, nombre del negocio y ciudad.
12. Fotos o videos de preparaciones reales y casos de uso.
13. Política de cambios, devoluciones y producto averiado.
14. Identificador de analítica (GA4, Plausible u otra opción) y acceso a Search Console.

## Siguiente fase recomendada

1. Validar todos los hechos comerciales anteriores con el dueño.
2. Incorporar ficha técnica descargable o un resumen público por producto.
3. Publicar una calculadora de costo por vaso basada en la dosis oficial.
4. Añadir prueba social real, no frases anónimas.
5. Medir `click_whatsapp`, `add_to_quote`, `send_quote`, `view_product` y `select_business`.
6. Comparar durante 30 días la versión actual contra QA usando clic a WhatsApp y cotizaciones enviadas como métricas primarias.
7. Expandir contenido solo con experiencia propia: recetas probadas, fotos, videos, rendimiento y preguntas reales de clientes. Google pide evidencia de experiencia directa y contenido creado para una audiencia real.[2]

## Criterio de éxito

La meta inicial no debe ser "#1 para todo". Debe ser:

- aumentar el porcentaje de visitantes que llega a una ficha o landing de segmento;
- aumentar clics cualificados a WhatsApp;
- aumentar cotizaciones enviadas;
- conocer la tasa de cierre por origen y tipo de negocio;
- ganar posiciones en consultas específicas que coinciden con el inventario real.

Si estas métricas no mejoran, la nueva copy no funciona, aunque suene mejor.

## Sources

[1] https://developers.google.com/search/docs/fundamentals/seo-starter-guide — SEO Starter Guide - Google Search Central
[2] https://developers.google.com/search/docs/fundamentals/creating-helpful-content — Creating helpful, reliable, people-first content - Google Search Central
[3] https://developers.google.com/search/docs/appearance/title-link — Influencing title links - Google Search Central
[4] https://developers.google.com/search/docs/appearance/snippet — Control snippets in search results - Google Search Central
[5] https://www.bubbleteacolombia.com/mayoristas — Insumos para bubble tea al por mayor en Colombia - Bubble Tea Colombia
[6] https://perlasexplosivas.com/bubble-tea-colombia — Bubble Tea Colombia: insumos y kits para tu negocio - LiquiPops
[7] https://www.bubbleplanet.com.co — Bubble Planet Colombia

---
name: "repo-baseline"
description: "Deja repos, sitios o software nuevos con su documentación mínima adaptada al proyecto (README, ARCHITECTURE, ADRs, DESIGN, ROADMAP con el norte del producto, legales AR, cookies y rastreo según la plataforma (web, móvil, escritorio, CLI), SECURITY, LICENSE, .gitignore/.gitattributes/.editorconfig y, en repos públicos u open source, CONTRIBUTING, CODE_OF_CONDUCT, plantillas de issues y PRs y CHANGELOG) y verifica qué falta."
---

# repo-baseline

Objetivo: que todo repo nazca con un set mínimo de documentación **escrita para ese proyecto**. Un README que dice "TODO: describir el proyecto" no sirve para nada. Uno que dice qué es, cómo se corre y dónde se despliega le ahorra horas a quien llegue después, incluido vos dentro de seis meses.

## El baseline

| Archivo | Cuándo | Qué contiene |
|---|---|---|
| `README.md` | Siempre | Qué es, para quién, cómo correrlo, cómo desplegarlo y links a los demás docs |
| `<carpeta>/README.md` | Cuando la carpeta tiene reglas propias (migrations, infra, scripts, legal, etc.) | Las reglas de esa carpeta |
| `ARCHITECTURE.md` | Siempre | Componentes, flujo de datos, dónde vive cada cosa y decisiones con link a su ADR |
| `docs/adr/0000-template.md` | Siempre | Plantilla de ADR |
| `docs/adr/0001-<decision>.md` | Siempre | Primera decisión real (normalmente el stack) |
| `DESIGN.md` | Solo si el diseño UX/UI está definido | Formato google-labs-code/design.md. Si no está definido, anotar el pendiente en el README |
| `ROADMAP.md` | Si el norte del producto está definido | El norte del producto, los pasos para llegar con su estado y el `## Deferred Backlog`. No es una lista de tareas. Si el norte no está definido, anotar el pendiente en el README |
| `PRIVACY.md` | Si maneja datos personales | Según la jurisdicción |
| `TERMS.md` | Si hay usuarios finales o venta | Según la jurisdicción |
| Botón de arrepentimiento | Si vende online en Argentina | Requisito de UI, no solo de docs |
| `COOKIES.md` | Si es **web** y usa rastreadores no esenciales (GA/GTM, Meta Pixel, Hotjar, Clarity, PostHog, Mixpanel…) | Tabla de cookies y SDKs con proveedor, finalidad, duración y tipo; cómo cambiar el consentimiento |
| Consentimiento de cookies (UI) | Web con rastreadores. Obligatorio con usuarios en UE/UK; si no, `recomendado` | Requisito de UI: banner previo a cargar los rastreadores, rechazar tan fácil como aceptar |
| Sección de rastreo en `PRIVACY.md` | App **móvil**, de **escritorio** o **CLI** con SDKs de analytics, publicidad o telemetría | SDK, dato, finalidad y cómo desactivarlo |
| ATT (iOS) | App móvil con un SDK que lee el IDFA (AppsFlyer, Adjust, Branch, Meta, AdMob) | `NSUserTrackingUsageDescription`: lo exige la App Store en cualquier jurisdicción |
| Opt-out de telemetría | Escritorio o CLI con telemetría | Flag o env var (`DO_NOT_TRACK`) documentada en PRIVACY |
| `SECURITY.md` | Siempre | Cómo reportar, qué datos se manejan, secretos y su rotación |
| `LICENSE.md` | Siempre | Según el titular. Default: propietario, "All rights reserved". Si es público u open source: la licencia OSI que elija el usuario, con su texto oficial completo |
| `.gitignore` | Siempre | Del stack real detectado |
| `.gitattributes` | Siempre | `* text=auto eol=lf` más los binarios y excepciones CRLF |
| `.editorconfig` | Siempre | Charset, fin de línea e indentación coherentes con `.gitattributes` y el estilo real del código |
| `CONTRIBUTING.md` | Si es público u open source | Cómo reportar bugs, los chequeos reales a correr antes de un PR y las reglas del repo |
| `CODE_OF_CONDUCT.md` | Si es público u open source | Texto **oficial** del Contributor Covenant, descargado (nunca de memoria) y con el contacto completado |
| `.github/PULL_REQUEST_TEMPLATE.md` | Si es público u open source en GitHub | Checklist con los chequeos reales del repo |
| `.github/ISSUE_TEMPLATE/` | Si es público u open source en GitHub | `bug_report.md` con los datos que hacen falta para reproducir, y `config.yml` que manda las vulnerabilidades al canal privado |
| `CHANGELOG.md` | Si publica versiones (campo `version`, tags de git) | Formato Keep a Changelog, con las versiones reales |
| `CODEOWNERS` | Si hay más de un mantenedor | Quién revisa cada carpeta |
| Reporte privado de vulnerabilidades | Si es público en GitHub | Es una configuración del repo, no un archivo: queda como `pendiente` en la tabla final con cómo activarlo |

Los esqueletos de cada documento están en el **Apéndice C**. Leelo antes de redactar.

## Flujo

### 1. Detectar antes de preguntar

Corré el check en modo JSON sobre la raíz del repo. El script está en el **Apéndice D**: escribilo en un archivo temporal **fuera del repo** (por ejemplo `check_baseline.py` en el directorio temporal del sistema), para no ensuciar el proyecto, y ejecutalo:

```bash
python <tmp>/check_baseline.py <repo> --json
```

Devuelve el stack detectado, los archivos del baseline presentes o faltantes, señales (pagos, auth, formularios, UI) y marcadores TODO-LEGAL existentes. Después leé lo que ya hay: `package.json`, `pyproject.toml`, `composer.json`, `Dockerfile`, configs de deploy (`vercel.json`, `wrangler.toml`, `netlify.toml`, workflows de CI), el README existente y `git remote -v`. Ahí suelen estar el nombre, el propósito, los comandos de run y build, el target de deploy y a veces el autor.

Inferir primero respeta el tiempo del usuario: cada dato que se puede leer del repo es una pregunta menos.

### 2. Preguntar solo lo que no se puede inferir, todo junto

Juntá las dudas en **un solo formulario** (AskUserQuestion si está disponible, con un máximo de 4 preguntas por formulario; si hacen falta más, un segundo formulario). Si no hay herramienta de formulario, mandá un único mensaje con las preguntas numeradas y opciones. No hagas preguntas sueltas una por una.

Candidatas, incluidas solo si no se pudieron inferir:

- **Titular del código:** agencia o estudio, cliente, o personal. Define LICENSE y quién figura en los legales.
- **Jurisdicción:** el default es **Argentina**, pero siempre se confirma con el usuario. Las opciones son Argentina, otra (cuál) o genérica.
- **¿Vende online?** Si la respuesta es sí y la jurisdicción es Argentina, aplica el botón de arrepentimiento.
- **¿Maneja datos personales?** Formularios, cuentas, newsletter, analytics con identificadores, etc.
- **¿El diseño UX/UI está definido?** Si no, DESIGN.md queda como pendiente.
- **¿Está definido el norte del producto?** Si sí, pedí el norte en una o dos frases y los pasos para llegar. Si no, ROADMAP.md queda como pendiente. Esta se pregunta siempre: el norte no se puede leer del repo.
- **¿Tiene usuarios en la UE o el Reino Unido?** Solo si el check encontró rastreadores en una plataforma web (`assumed.platforms` incluye `web` y `assumed.trackers` no está vacío). Define si el banner de consentimiento es obligatorio o recomendado.
- **¿Dónde se despliega?** Solo si no hay config de deploy en el repo.
- **¿Es público u open source?** Define los archivos de comunidad (CONTRIBUTING, CODE_OF_CONDUCT, plantillas) y la licencia. Se infiere de una licencia OSI en `LICENSE` (el check lo reporta como `assumed.public`) o de `gh repo view --json visibility`; si no hay ninguna de las dos, se pregunta.

Si las señales del check ya responden algo (por ejemplo, `mercadopago` en las dependencias indica que vende online), presentalo como opción preseleccionada para que el usuario confirme, en lugar de preguntarlo de cero.

### 3. Verificar la normativa vigente (solo si hay legales)

Las normas cambian; por ejemplo, la Res. SCI 424/2020 fue derogada en 2025. Antes de redactar PRIVACY, TERMS o algo sobre el botón de arrepentimiento:

1. Leé el **Apéndice A** (Argentina) o el **Apéndice B** (otras jurisdicciones o genérica).
2. Si tenés búsqueda web, confirmá que cada norma citada siga vigente, sobre todo si la fecha de "última verificación" del archivo tiene más de 6 meses. Si encontrás un cambio, usá la norma nueva y avisale al usuario.
3. Si no podés verificar, citá igual lo que dice la referencia, agregá en el documento `> Normativa verificada al <fecha de la referencia> — confirmar vigencia antes de publicar` e incluilo en la tabla final.

### 4. Redactar

Reglas que importan, con su porqué:

- **Contenido real, no relleno.** Cada sección se escribe con lo que dice el repo: comandos reales de `scripts` en package.json, variables reales de `.env.example` y carpetas reales. Si de verdad falta un dato técnico, poné `TODO: <qué falta y dónde averiguarlo>`.
- **Nunca inventes datos legales.** Razón social, CUIT, domicilio, email legal, nombre del responsable, número de registro de base de datos, tribunales competentes: todo eso va como marcador visible `TODO-LEGAL: <dato>`. Un CUIT inventado en unos términos publicados es peor que un hueco visible, porque nadie lo va a revisar.
- **Las decisiones no se fabrican.** En el ADR 0001, el contexto y la decisión salen de la evidencia del repo. Si el usuario no dio las alternativas descartadas, podés proponer las obvias, pero marcalas `(sugerido — confirmar)` para que no pasen por hechos.
- **El norte no se fabrica.** El norte y los pasos de ROADMAP.md salen de lo que dijo el usuario, nunca de TODOs ni de la estructura del código. Lo único que sí sale del repo es el estado de cada paso (`hecho`, `en curso`, `pendiente`). Si hay un plan por etapas (`docs/specs/*/plan.md`), el paso enlaza a ese plan en lugar de copiar sus tareas.
- **Fuentes en los ADRs:** links a la documentación oficial de las tecnologías elegidas. Solo URLs que existan; si no podés verificar una, no la pongas.
- **Idioma:** el que use el usuario o el del README existente. Los nombres de archivo van en inglés y mayúsculas, como en la tabla.
- **Textos normativos de terceros, descargados.** El Code of Conduct (y cualquier licencia OSI) se baja de su fuente oficial y se copia tal cual; solo se completan sus placeholders (por ejemplo `[INSERT CONTACT METHOD]`). No se reconstruye de memoria ni se traduce: si hace falta otro idioma y no hay traducción oficial a mano, el archivo en ese idioma resume y enlaza al texto que rige. Ver Apéndice C.
- **Los chequeos de CONTRIBUTING y de la plantilla de PR son los reales.** Salen del CI y de los scripts del repo; un comando que no existe en el repo no va.
- **Botón de arrepentimiento:** además de documentarlo en TERMS.md, buscá en el código si ya existe (el check lo reporta). Si no existe, agregá una fila "pendiente de implementación en UI" en la tabla final con los requisitos del Apéndice A. No lo implementes salvo que el usuario lo pida: es código de producto, no documentación.
- **Cookies y rastreo dependen de la plataforma, no de "si es web".** El check informa `assumed.platforms` (`web`, `mobile`, `desktop`, `cli`) y `assumed.trackers`, y exige lo que corresponde a esa combinación: web → `COOKIES.md` y banner; móvil → sección en PRIVACY y ATT si hay IDFA; escritorio o CLI → sección en PRIVACY y opt-out. La tabla de `COOKIES.md` y la sección de PRIVACY se arman con los rastreadores detectados; la duración de cada cookie sale de la doc del proveedor, y si no la podés verificar va `TODO: duración`. La analítica sin cookies (Plausible, Fathom, Vercel Analytics, Cloudflare Web Analytics) solo se declara en PRIVACY. El banner, el opt-out y el prompt de ATT son código de producto: igual que el botón de arrepentimiento, quedan como "pendiente de implementación" y no se implementan salvo pedido.

### 5. Archivos que ya existen: diff, nunca sobrescribir

Si un archivo del baseline ya existe, no lo pises. Leelo, armá la versión mejorada y mostrale al usuario un **diff unificado** en el chat (o un resumen de secciones agregadas si el diff es muy largo). Aplicalo solo con su OK explícito. La razón: ese archivo puede tener decisiones o texto legal revisado por alguien, y una sobrescritura silenciosa lo destruye.

`.gitignore` y `.gitattributes` existentes: proponé solo las líneas que faltan (append), no un reemplazo.

### 6. Verificar

Corré el check de nuevo, ahora en modo tabla, con los flags que correspondan según las respuestas:

```bash
python <tmp>/check_baseline.py <repo> --[no-]sells-online --[no-]personal-data --[no-]ui-defined --[no-]roadmap-defined --[no-]public --[no-]eu-users --jurisdiction AR
```

Pasá siempre las respuestas confirmadas como flags, incluidas las negativas. Sin flags, el script adivina a partir de señales del código (por ejemplo, una integración con WooCommerce parece venta online aunque no lo sea), y esa adivinanza no debe pisar lo que dijo el usuario.

`CODEOWNERS` y el reporte privado de vulnerabilidades no los verifica el script: revisalos a mano si aplican.

Si reporta faltantes que deberías haber creado, resolvelos antes de cerrar.

### 7. Cerrar con la tabla

Terminá **siempre** con esta tabla, una fila por archivo del baseline:

| Archivo | Estado | Falta completar |
|---|---|---|
| README.md | creado | — |
| LICENSE.md | creado | TODO-LEGAL: razón social del titular |
| PRIVACY.md | diff propuesto | Esperando OK |
| DESIGN.md | pendiente | Diseño UX/UI no definido; anotado en README |
| ROADMAP.md | pendiente | Norte del producto no definido; anotado en README |
| CODE_OF_CONDUCT.md | creado | Confirmar el contacto para reportes |
| Reporte privado de vulnerabilidades | pendiente | Activarlo: Settings → Security → Private vulnerability reporting, o `gh api -X PUT repos/<owner>/<repo>/private-vulnerability-reporting` |

Estados válidos: `creado`, `actualizado`, `diff propuesto`, `pendiente`, `recomendado`, `no aplica`.

Debajo, la lista consolidada de **todos** los `TODO-LEGAL` con archivo y dato, para que el usuario se los pase de una al contador o al cliente.

## Límites

- **No ejecutes `git add`, `git commit` ni `git push`**, ni nada que modifique el estado de git (`git init`, `checkout`, `stash`). El usuario revisa y commitea. Leer (`git remote -v`, `git log`) está bien.
- No instales dependencias ni modifiques código de la app.
- El alcance es solo documentación: no audites ni comentes el código de la app (vulnerabilidades, bugs, versiones). Las únicas excepciones son las que cubre el propio baseline: `.env` sin ignorar en `.gitignore` y la presencia o ausencia del botón de arrepentimiento.
- No borres archivos.
- No cambies configuraciones del repo remoto (visibilidad, reporte de vulnerabilidades, protección de ramas): se dejan como `pendiente` en la tabla, con el comando, para que las aplique el usuario.

---

## Apéndice A — Referencia legal Argentina

**Última verificación: 2026-10-08.** Si pasaron más de 6 meses, reverificá con búsqueda web antes de citar.
Esto no es asesoramiento legal: los documentos generados son borradores para que los revise un abogado.

### Normas a citar

| Norma | Qué regula | Estado al 2026-10-08 |
|---|---|---|
| Ley 24.240 de Defensa del Consumidor | Relación de consumo, información al consumidor y revocación (art. 34) | Vigente |
| Código Civil y Comercial, arts. 1110 y ss. | Revocación en contratos a distancia: 10 días corridos | Vigente |
| Disposición SSDCyLC 954/2025 (Subsecretaría de Defensa del Consumidor y Lealtad Comercial) | Botón de arrepentimiento y baja de servicios. **Deroga y unifica** la Res. SCI 424/2020 y la Res. 316/2018 | Vigente desde septiembre de 2025 (verificado en fuentes secundarias) |
| Disposición DNDCYAC 3/2026 | Verificación de identidad al usar el botón | Mencionada como relacionada; confirmar alcance |
| Ley 25.326 de Protección de Datos Personales | Datos personales: información al titular (art. 6), acceso (art. 14) y rectificación/supresión (art. 16) | Vigente; hay proyectos de reforma en trámite, revisar |
| Decreto 1558/2001 | Reglamentario de la Ley 25.326 | Vigente |
| AAIP (Agencia de Acceso a la Información Pública) | Autoridad de control de datos personales | Confirmar al redactar |

**No cites la Res. SCI 424/2020 como vigente.** Si un repo existente la cita, proponé el cambio en el diff.

**Cookies en Argentina:** ninguna norma vigente exige un banner de consentimiento. Las cookies y la analítica se declaran en PRIVACY.md (art. 6 de la Ley 25.326: qué datos, finalidad y destinatarios). Si el sitio tiene usuarios en la UE o el Reino Unido, se suman los requisitos del Apéndice B.

### Botón de arrepentimiento (si vende online)

Requisitos según la Disp. 954/2025:

- Debe estar visible desde el **primer acceso** del sitio o app, en un lugar destacado.
- **Sin registro previo** ni trámites adicionales para usarlo.
- El proveedor responde **por el mismo medio dentro de las 24 h** con un **código de identificación** de la solicitud.
- Plazo para arrepentirse: **10 días corridos** desde la entrega del bien o la celebración del contrato, lo que ocurra último (art. 34 de la Ley 24.240 y art. 1110 del CCyC).
- Hay excepciones (bienes personalizados o perecederos, software y archivos digitales de uso permanente, etc.). Listalas en TERMS.md solo si aplican al producto.
- Si vende servicios con suscripción, también corresponde una vía de baja igual de simple.

En TERMS.md: una sección "Derecho de arrepentimiento" con el plazo, cómo ejercerlo (link al botón) y quién paga los gastos de devolución (a cargo del proveedor según el art. 1115 del CCyC; marcar `[confirmar con abogado]`).

### Datos del titular que exige la ley (todos TODO-LEGAL si no los dio el usuario)

- Razón social o nombre del titular
- CUIT
- Domicilio legal
- Email de contacto para consumidores y para ejercer los derechos ARCO
- Para PRIVACY: responsable de la base de datos y, si corresponde, número de inscripción en el registro de la AAIP
- Leyenda de la AAIP sobre el derecho de acceso (art. 14 inc. 3 de la Ley 25.326). Es una leyenda estándar: confirmá el texto vigente en el sitio de la AAIP antes de copiarlo, no lo reconstruyas de memoria.
- Link a la Ventanilla Única Federal de Defensa del Consumidor (sitios de venta). Confirmá la URL vigente.

### PRIVACY.md — contenido mínimo (art. 6 de la Ley 25.326)

1. Qué datos se recolectan, mapeados a lo que realmente hace el código (formularios, auth, analytics, cookies).
2. Finalidad de cada uno.
3. Destinatarios o terceros: proveedores reales detectados (hosting, analytics, pagos, email).
4. Identidad y domicilio del responsable (TODO-LEGAL).
5. Si es obligatorio darlos y qué pasa si no se dan.
6. Derechos de acceso, rectificación y supresión, y cómo ejercerlos: acceso gratuito cada 6 meses, respuesta en 10 días corridos; rectificación en 5 días hábiles.
7. Transferencias internacionales, si el hosting está fuera de Argentina, lo que es muy común en Vercel, Cloudflare, AWS, etc.
8. Plazo de conservación.

---

## Apéndice B — Jurisdicción genérica u otra

Usala cuando la jurisdicción no es Argentina o el usuario eligió "genérica".

### Si el usuario nombró otra jurisdicción

No tenés una referencia verificada acá. Con búsqueda web disponible, identificá la ley de protección de datos y la de consumidor vigentes y citalas con link oficial. Sin búsqueda web, no cites normas de memoria: poné `TODO-LEGAL: normativa aplicable en <jurisdicción>`.

Referencias habituales (confirmá su vigencia antes de citarlas):

- UE: GDPR (Reglamento UE 2016/679) y derecho de desistimiento de 14 días (Directiva 2011/83/UE).
- Chile: Ley 19.628 de datos y Ley 19.496 del consumidor. Ojo: la ley de datos fue reformada; verificar.
- Uruguay: Ley 18.331.
- México: LFPDPPP. Fue reemplazada en 2025; verificar.

### Plantilla genérica

PRIVACY.md con la misma estructura de 8 puntos que el Apéndice A, pero sin citar artículos: "conforme a la normativa aplicable en `TODO-LEGAL: jurisdicción`".

TERMS.md: objeto, uso aceptable, propiedad intelectual, limitación de responsabilidad, modificaciones, ley aplicable y jurisdicción (`TODO-LEGAL`), y contacto.

Agregá arriba de cada documento: `> Borrador generado sin jurisdicción definida. Revisar con un abogado antes de publicar.`

### Cookies y rastreo con usuarios en la UE o el Reino Unido

Aplica aunque la jurisdicción del titular sea otra. Confirmá su vigencia antes de citarlas, como las demás:

- UE: Directiva 2002/58/CE (ePrivacy), art. 5(3). Guardar o leer información en el dispositivo requiere consentimiento previo, salvo que sea estrictamente necesario para el servicio. Abarca cookies, localStorage, SDKs móviles y fingerprinting. El consentimiento sigue el GDPR (art. 4(11) y art. 7): libre, específico, informado, sin casillas premarcadas, tan fácil de retirar como de dar.
- Reino Unido: PECR, reg. 6, con el mismo esquema. La Data (Use and Access) Act 2025 sumó excepciones para analítica de bajo riesgo: verificar su entrada en vigor antes de apoyarse en ellas.
- Requisitos del banner: los rastreadores no cargan antes de aceptar; "Rechazar" visible en la primera capa, al mismo nivel que "Aceptar"; nada de muros de cookies; una forma de cambiar la elección después (link en el footer).

---

## Apéndice C — Esqueletos de los documentos

Son estructuras, no texto para copiar. Cada sección se llena con datos del repo. Una sección que no aplica se omite; no se deja vacía.

### Índice
1. README.md
2. README por carpeta
3. ARCHITECTURE.md
4. ADR (template y 0001)
5. DESIGN.md
6. ROADMAP.md
7. SECURITY.md
8. LICENSE.md
9. .gitignore
10. .gitattributes
11. .editorconfig
12. CONTRIBUTING.md
13. CODE_OF_CONDUCT.md
14. Plantillas de issues y PRs
15. CHANGELOG.md
16. CODEOWNERS
17. COOKIES.md y sección de rastreo en PRIVACY.md

---

### 1. README.md

```markdown
# <Nombre del proyecto>

<Una o dos frases: qué es y qué problema resuelve.>

**Para quién:** <usuarios o cliente>
**Estado:** <en desarrollo / producción / etc.>

## Requisitos
<runtime y versión reales: node >=20 según engines, python 3.12 según pyproject, etc.>

## Cómo correrlo
<comandos reales: install, configurar .env a partir de .env.example y dev>

## Cómo desplegarlo
<target real (Vercel, Cloudflare, VPS, Docker) y pasos o pipeline. Si no se sabe: TODO>

## Documentación
- [Arquitectura](ARCHITECTURE.md)
- [Decisiones (ADRs)](docs/adr/)
- [Diseño](DESIGN.md) — o "Pendiente: el diseño UX/UI todavía no está definido"
- [Roadmap](ROADMAP.md) — o "Roadmap pendiente: el norte del producto todavía no está definido"
- [Seguridad](SECURITY.md)
- [Privacidad](PRIVACY.md) · [Términos](TERMS.md) · [Cookies](COOKIES.md)  ← solo si existen
- [Licencia](LICENSE.md)
```

### 2. README por carpeta

Solo cuando la carpeta tiene reglas que alguien podría romper sin saberlo. Ejemplos: `migrations/` (nunca editar una migración aplicada), `infra/` (cómo se aplica y quién puede), `scripts/` (qué hace cada uno y si es destructivo), `public/legal/`, o carpetas de contenido generado. Tres a diez líneas: propósito, reglas y cómo agregar algo.

### 3. ARCHITECTURE.md

```markdown
# Arquitectura

## Visión general
<2-4 frases y, si ayuda, un diagrama mermaid simple>

## Componentes
| Componente | Responsabilidad | Ubicación |
|---|---|---|

## Flujo de datos
<cómo viaja un request o un dato real: del usuario al frontend, a la API, a la DB y a terceros>

## Dónde vive cada cosa
<mapa de carpetas real, solo las relevantes>

## Servicios externos
<hosting, DB, pagos, email, analytics detectados>

## Decisiones
- [ADR-0001: <título>](docs/adr/0001-<slug>.md)
```

### 4. ADR

`docs/adr/0000-template.md`:

```markdown
# ADR-NNNN: <Título corto en imperativo>

- **Estado:** propuesto | aceptado | reemplazado por ADR-XXXX
- **Fecha:** YYYY-MM-DD

## Contexto
<qué problema o fuerza obliga a decidir>

## Decisión
<qué se decidió, en una o dos frases>

## Alternativas descartadas
| Alternativa | Motivo del descarte |
|---|---|

## Consecuencias
<positivas, negativas y qué queda atado a esta decisión>

## Fuentes
- <links a documentación oficial>
```

`0001-<slug>.md`: la primera decisión real, normalmente el stack o la plataforma de deploy, con la fecha de hoy. El slug va en kebab-case (por ejemplo `0001-usar-nextjs-en-vercel.md`).

### 5. DESIGN.md (formato google-labs-code/design.md, versión alpha)

Spec: https://github.com/google-labs-code/design.md. Lint: `npx @google/design.md lint DESIGN.md`.

Solo cuando el diseño está definido (paleta, tipografía y componentes decididos, por ejemplo en Figma o en un tailwind.config con tokens). No inventes colores.

```markdown
---
version: alpha
name: <Nombre del sistema>
description: <opcional>
colors:
  primary: "#......"
typography:
  body:
    fontFamily: <...>
    fontSize: <...>
rounded:
  md: 8px
spacing:
  md: 16px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
---

## Overview
## Colors
## Typography
## Layout
## Elevation & Depth
## Shapes
## Components
## Do's and Don'ts
```

Las secciones pueden omitirse, pero las que aparecen tienen que respetar este orden y no pueden duplicarse. Si los tokens salen de `tailwind.config` o de variables CSS del repo, usá esos valores.

### 6. ROADMAP.md

Solo cuando el usuario definió el norte del producto. Marca hacia dónde va el producto y el camino para llegar; no es una lista de tareas ni un changelog. Las tareas viven en el plan de cada paso y las versiones publicadas, en CHANGELOG.md. Si el norte no está definido, no se crea: se anota el pendiente en el README.

```markdown
# Roadmap

## Norte
<qué es el producto cuando está terminado y para quién, en una o dos frases, con las palabras del usuario>

## Pasos
1. <hito> — hecho. Plan: [docs/specs/<ciclo>/plan.md](docs/specs/<ciclo>/plan.md)
2. <hito> — en curso
3. <hito> — pendiente

## Deferred Backlog
- <lo que se posterga a propósito y por qué>
```

Los pasos y su orden los da el usuario. El estado (`hecho`, `en curso`, `pendiente`) sale de la evidencia del repo. Si existe `docs/specs/*/plan.md`, cada paso enlaza a su plan en vez de copiar el detalle. `## Deferred Backlog` se omite si no hay nada postergado.

### 7. SECURITY.md

```markdown
# Seguridad

## Cómo reportar una vulnerabilidad
<email o canal; TODO si no se sabe. Qué incluir y tiempo de respuesta esperado.>
No abrir issues públicos con vulnerabilidades.

## Datos que maneja el sistema
| Dato | Clasificación | Dónde se guarda | Quién accede |
|---|---|---|---|

## Secretos
| Secreto | Dónde vive | Rotación | Responsable |
|---|---|---|---|
<sale de .env.example y de la config de deploy: variables de Vercel/Cloudflare, GitHub Actions secrets, etc.>

- Nunca commitear `.env`; el repo incluye `.env.example` sin valores.
- Ante una filtración: revocar, rotar, revisar logs de acceso y documentar.

## Dependencias
<cómo se actualizan: Dependabot o Renovate, o TODO>
```

### 8. LICENSE.md

Default (sin otra indicación del usuario), propietario:

```markdown
Copyright (c) <año> <titular | TODO-LEGAL: razón social del titular>

All rights reserved.

Este software y su documentación son propiedad exclusiva del titular. Queda prohibida su copia, modificación, distribución o uso sin autorización previa y por escrito del titular.
```

Si el titular es el cliente, pero la agencia desarrolla, agregá una nota sobre la cesión de derechos según el contrato (`TODO-LEGAL: referencia al contrato`). Si el usuario elige una licencia open source, usá el texto oficial completo de esa licencia, no un resumen.

### 9. .gitignore

Del stack detectado, combinando secciones. Siempre incluir:

```
# Secretos
.env
.env.*
!.env.example

# SO / editores
.DS_Store
Thumbs.db
.vscode/*
!.vscode/extensions.json
.idea/
```

Más lo específico del stack: Node (`node_modules/`, `dist/`, `.next/`, `.vercel/`, `.wrangler/`, `*.log`), Python (`__pycache__/`, `.venv/`, `*.pyc`, `.pytest_cache/`), PHP (`vendor/`), .NET (`bin/`, `obj/`), Terraform (`.terraform/`, `*.tfstate*`, `*.tfvars` salvo ejemplos), etc.

### 10. .gitattributes

```
* text=auto eol=lf

# Scripts de Windows necesitan CRLF
*.bat text eol=crlf
*.cmd text eol=crlf
*.ps1 text eol=crlf

# Binarios
*.png binary
*.jpg binary
*.jpeg binary
*.gif binary
*.webp binary
*.ico binary
*.pdf binary
*.woff binary
*.woff2 binary
*.zip binary
```

Agregá `*.ps1` solo si hay scripts PowerShell; el resto de las extensiones, solo si están en el repo o son típicas del stack.

### 11. .editorconfig

```ini
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
indent_style = space
indent_size = 2

[*.md]
trim_trailing_whitespace = false
```

Ajustá `indent_size` por extensión al estilo real del código (Python 4, Go con tabs, Makefile con tabs). Si `.gitattributes` fija CRLF para alguna extensión, repetilo acá (`end_of_line = crlf`).

### 12. CONTRIBUTING.md

```markdown
# Contributing

<Una línea: qué contribuciones son bienvenidas.> Al participar aceptás el
[Code of Conduct](CODE_OF_CONDUCT.md). Las vulnerabilidades van por el canal
privado de [SECURITY.md](SECURITY.md), no por issues.

## Reportar un bug
<qué datos hacen falta para reproducir: versiones, comando, salida; qué tapar (secretos, IPs)>

## Antes de abrir un pull request
<los comandos reales del CI y de los scripts del repo, en bloque de código>
<cómo probar un cambio de verdad, si los tests no alcanzan>

## Reglas del repo
<las reglas que un contribuidor externo podría romper sin saberlo, cada una con su porqué; link a los ADRs>

## Commits y pull requests
<convención real de commits del repo (mirá `git log`), un tema por PR, CI en verde>
```

### 13. CODE_OF_CONDUCT.md

No se redacta: se descarga el texto oficial del Contributor Covenant (versión vigente; la 2.1 está en `https://raw.githubusercontent.com/EthicalSource/contributor_covenant/release/content/version/2/1/code_of_conduct.md`).

1. Bajalo a un directorio temporal y leelo entero.
2. Sacale el bloque de metadatos del principio (`+++ ... +++`) si lo trae.
3. Reemplazá `[INSERT CONTACT METHOD]` por un canal **privado** de contacto. Si el usuario no dio ninguno, poné el que haya (por ejemplo el perfil de GitHub del mantenedor) y agregá una fila en la tabla final para confirmarlo.
4. Si no podés descargarlo, no lo escribas de memoria: dejá el archivo como `pendiente` en la tabla, con el link oficial.

Para otro idioma, enlazá la traducción oficial (`https://www.contributor-covenant.org/translations`) desde un archivo corto en ese idioma, que diga que el texto que rige es el del archivo principal.

### 14. Plantillas de issues y PRs

`.github/ISSUE_TEMPLATE/bug_report.md`:

```markdown
---
name: Bug report
about: Algo no funciona como dice la documentación
labels: bug
---

**Versiones:** <las que importan para este proyecto: runtime, plataforma, SO>
**Qué hiciste:** <comando o pasos>
**Qué esperabas y qué pasó:** <incluí la salida o el error>
**Contexto:** <config relevante, sin secretos ni datos reales>
```

`.github/ISSUE_TEMPLATE/config.yml`:

```yaml
blank_issues_enabled: true
contact_links:
  - name: Reportar una vulnerabilidad
    url: https://github.com/<owner>/<repo>/security/advisories/new
    about: No abras un issue público: usá el reporte privado.
```

`.github/PULL_REQUEST_TEMPLATE.md`:

```markdown
## Qué cambia y por qué

## Cómo lo probaste
- [ ] <cada chequeo real del CI, uno por línea>
- [ ] <prueba manual, si el repo la pide en CONTRIBUTING>

## Docs
- [ ] Actualicé la documentación afectada (y su versión en otro idioma, si existe)
```

### 15. CHANGELOG.md

Formato [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/). Las versiones salen de los tags de git o del campo `version`; no inventes fechas ni entradas: si el historial no alcanza para reconstruir versiones viejas, empezá por la actual.

```markdown
# Changelog

Todos los cambios notables de este proyecto se documentan en este archivo.
El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y el proyecto usa [Semantic Versioning](https://semver.org/lang/es/).

## [Unreleased]

## [<versión>] - <YYYY-MM-DD>
### Added
- <lo que agregó esa versión, según los commits o el tag>
```

### 16. CODEOWNERS

Solo con más de un mantenedor; con uno solo no agrega nada. Va en `.github/CODEOWNERS`, con usuarios o equipos reales (`* @owner`, `/infra/ @team-infra`). Los nombres de usuario no se inventan: si no los dio el usuario, no se crea el archivo.

### 17. COOKIES.md y sección de rastreo en PRIVACY.md

Cuál de los dos corresponde lo decide la plataforma (paso 4). Las filas salen de `assumed.trackers` y del código: una por cookie o SDK real, nunca un catálogo genérico.

COOKIES.md (web):

```markdown
# Política de cookies

Última actualización: <YYYY-MM-DD>

## Qué son
Una o dos frases: archivos o identificadores que el sitio guarda en tu navegador.

## Qué usamos
| Nombre | Proveedor | Finalidad | Duración | Tipo |
|---|---|---|---|---|
| `_ga`, `_ga_<ID>` | Google Analytics | Medir visitas | 2 años | Analítica |
| `<sesión>` | Propia | Mantener la sesión iniciada | Sesión | Esencial |

Las esenciales no necesitan consentimiento; las demás solo se cargan si las aceptás.

## Cómo cambiar tu elección
Dónde está el link para reabrir el panel (por ejemplo, el footer) y cómo borrar las cookies desde el navegador.

## Más información
[Política de privacidad](PRIVACY.md) · contacto: TODO-LEGAL: email de contacto
```

Sección en PRIVACY.md (móvil, escritorio o CLI):

```markdown
## Rastreo y telemetría

| SDK | Qué dato envía | Para qué | Cómo desactivarlo |
|---|---|---|---|
| PostHog | Eventos de uso anónimos, versión, SO | Priorizar mejoras | `DO_NOT_TRACK=1` o Ajustes → Privacidad |
```

En iOS, si un SDK lee el IDFA, la fila aclara que se pide permiso con el diálogo de App Tracking Transparency y que sin ese permiso no se usa.

---

## Apéndice D — check_baseline.py

Solo usa la biblioteca estándar de Python 3.9+, así que corre igual en Windows, Linux y macOS. Copialo tal cual.

```python
#!/usr/bin/env python3
"""check_baseline.py — reports which repo-baseline files are missing in a repository.

Usage:
    python check_baseline.py [REPO] [--json] [--[no-]sells-online] [--[no-]personal-data]
                             [--[no-]ui-defined] [--[no-]roadmap-defined] [--[no-]public]
                             [--[no-]eu-users] [--jurisdiction AR|EU|UK|OTHER|GENERIC]

Without flags, sells-online / personal-data are guessed from code signals. Pass the
user's confirmed answers as flags so the verdict reflects reality, not the guess.

Exit code: 0 if every required item is present, 1 otherwise.
Standard library only, so it runs the same on Windows, Linux and macOS.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build",
             ".next", ".nuxt", "vendor", ".terraform", "bin", "obj", ".wrangler", ".vercel",
             "coverage", ".cache", "target", "Pods", "graphify-out"}
TEXT_EXT = {".md", ".txt", ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte", ".astro",
            ".html", ".php", ".py", ".json", ".yml", ".yaml", ".toml", ".cs", ".go", ".rb",
            ".dart", ".kt", ".kts", ".gradle", ".swift", ".plist", ".xml"}
MAX_FILES = 5000
MIN_CONTENT_BYTES = 200  # files smaller than this are flagged as "casi vacío"

SIGNALS = {
    "payments": ["mercadopago", "stripe", "paypal", "@shopify", "woocommerce", "checkout",
                 "mobbex", "payway", "todopago", "uala"],
    "auth": ["next-auth", "@auth/", "passport", "firebase/auth", "@supabase/auth", "clerk",
             "auth0", "django.contrib.auth", "flask-login", "lucia", "jsonwebtoken"],
    "forms": ["<form", "react-hook-form", "formik", "formspree", "resend", "nodemailer",
              "sendgrid"],
    # Store or read identifiers on the user's device for non-essential purposes (ePrivacy art. 5(3)).
    "trackers": ["gtag(", "googletagmanager", "google-analytics", "react-ga", "@next/third-parties/google",
                 "fbq(", "connect.facebook.net", "hotjar", "clarity.ms", "analytics.tiktok.com",
                 "snap.licdn.com", "posthog", "mixpanel", "amplitude", "@segment/", "analytics-node",
                 "@aptabase", "electron-google-analytics", "universal-analytics", "applicationinsights",
                 "firebase/analytics", "@react-native-firebase/analytics", "firebase_analytics",
                 "firebase-analytics", "appsflyer", "react-native-adjust", "com.adjust.sdk", "adjust_sdk",
                 "react-native-branch", "io.branch", "react-native-fbsdk", "facebook_app_events",
                 "com.facebook.android", "google-mobile-ads", "google_mobile_ads", "play-services-ads"],
    # Analytics without cookies or device identifiers: declared in PRIVACY, no consent banner.
    "cookieless": ["plausible", "usefathom", "@vercel/analytics", "cloudflareinsights", "umami",
                   "simpleanalytics", "goatcounter"],
    "ui": [".tsx", ".jsx", ".vue", ".svelte", ".astro", ".html", "tailwind.config"],
}
# Signals that docs would trigger just by describing them (a PRIVACY.md that names PostHog).
CODE_ONLY_SIGNALS = {"trackers", "cookieless"}
# Mobile SDKs that read the IDFA: iOS requires the App Tracking Transparency prompt.
IDFA_SDKS = ["appsflyer", "react-native-adjust", "com.adjust.sdk", "adjust_sdk", "react-native-branch",
             "io.branch", "react-native-fbsdk", "facebook_app_events", "google-mobile-ads",
             "google_mobile_ads", "adsupport"]
CONSENT = re.compile(r"cookieconsent|cookie-consent|klaro|osano|cookiebot|onetrust|consent-manager"
                     r"|gtag\(\s*['\"]consent", re.I)
TELEMETRY_OPTOUT = re.compile(r"DO_NOT_TRACK|no-telemetry|TELEMETRY_DISABLED|DISABLE_TELEMETRY"
                              r"|telemetry\s*[:=]\s*false|opt_?out", re.I)
ATT_KEY = re.compile(r"NSUserTrackingUsageDescription")
PRIVACY_TRACKING = re.compile(r"^#+ .*(cookies|rastreo|telemetr|tracking|seguimiento)", re.I | re.M)
ARREPENTIMIENTO = re.compile(r"arrepentimiento", re.I)
TODO_LEGAL = re.compile(r"TODO-LEGAL")
OBSOLETE_NORMS = {"424/2020": "Res. SCI 424/2020 derogada por Disp. SSDCyLC 954/2025",
                  "316/2018": "Res. 316/2018 derogada por Disp. SSDCyLC 954/2025"}


def walk(repo: Path):
    count = 0
    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".") or d in {".github"}]
        for f in files:
            yield Path(root) / f
            count += 1
            if count >= MAX_FILES:
                return


def read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def detect_stack(repo: Path) -> list[str]:
    stack = []
    pkg = repo / "package.json"
    if pkg.exists():
        stack.append("node")
        try:
            data = json.loads(read(pkg) or "{}")
            deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
            for name, label in [("next", "nextjs"), ("react", "react"), ("vue", "vue"),
                                ("astro", "astro"), ("svelte", "svelte"), ("vite", "vite"),
                                ("express", "express"), ("@nestjs/core", "nestjs"),
                                ("wrangler", "cloudflare-workers"), ("typescript", "typescript"),
                                ("nuxt", "nuxt"), ("electron", "electron"), ("@tauri-apps/api", "tauri"),
                                ("react-native", "react-native"), ("expo", "expo"),
                                ("@capacitor/core", "capacitor")]:
                if name in deps:
                    stack.append(label)
        except json.JSONDecodeError:
            pass
    markers = {
        "python": ["pyproject.toml", "requirements.txt", "setup.py", "Pipfile"],
        "php": ["composer.json"], "go": ["go.mod"], "rust": ["Cargo.toml"], "flutter": ["pubspec.yaml"],
        "ruby": ["Gemfile"], "java": ["pom.xml", "build.gradle", "build.gradle.kts"],
        "docker": ["Dockerfile", "docker-compose.yml", "compose.yaml"],
        "vercel": ["vercel.json"], "cloudflare": ["wrangler.toml", "wrangler.jsonc"],
        "netlify": ["netlify.toml"],
    }
    for label, files in markers.items():
        if any((repo / f).exists() for f in files):
            stack.append(label)
    if any(repo.glob("*.csproj")) or any(repo.glob("*.sln")):
        stack.append("dotnet")
    if any(repo.glob("*.tf")) or any(repo.glob("infra/**/*.tf")):
        stack.append("terraform")
    if (repo / "src-tauri").is_dir() and "tauri" not in stack:
        stack.append("tauri")
    if (repo / "index.html").exists() and "node" not in stack:
        stack.append("static-html")
    if (repo / ".github" / "workflows").is_dir():
        stack.append("github-actions")
    return stack


def scan(repo: Path) -> dict:
    signals = {k: [] for k in SIGNALS}
    todo_legal: dict[str, int] = {}
    arrepentimiento_in_code: list[str] = []
    consent_in_code: list[str] = []
    optout_in_code: list[str] = []
    att_declared: list[str] = []
    idfa_sdks: list[str] = []
    tracker_names: set[str] = set()
    obsolete: list[dict] = []
    for p in walk(repo):
        rel = p.relative_to(repo).as_posix()
        if p.suffix.lower() in {".tsx", ".jsx", ".vue", ".svelte", ".astro", ".html"} \
                and len(signals["ui"]) < 5:
            signals["ui"].append(rel)
        if p.suffix.lower() not in TEXT_EXT and p.name not in {"tailwind.config.js", "tailwind.config.ts"}:
            continue
        if p.stat().st_size > 1_000_000:
            continue
        text = read(p)
        # "actions/checkout" (GitHub Actions) is not a payment checkout.
        low = text.lower().replace("actions/checkout", "")
        is_doc = p.suffix.lower() in {".md", ".txt"}
        for key, needles in SIGNALS.items():
            if key == "ui" or (is_doc and key in CODE_ONLY_SIGNALS):
                continue
            if key == "trackers":
                tracker_names.update(n for n in needles if n in low)
            for n in needles:
                if n in low and len(signals[key]) < 5 and rel not in signals[key]:
                    signals[key].append(rel)
                    break
        if p.name.startswith("tailwind.config") and rel not in signals["ui"]:
            signals["ui"].append(rel)
        n_todo = len(TODO_LEGAL.findall(text))
        if n_todo:
            todo_legal[rel] = n_todo
        if p.suffix.lower() != ".md" and ARREPENTIMIENTO.search(text):
            arrepentimiento_in_code.append(rel)
        if not is_doc:
            if CONSENT.search(text):
                consent_in_code.append(rel)
            if TELEMETRY_OPTOUT.search(text):
                optout_in_code.append(rel)
            if ATT_KEY.search(text):
                att_declared.append(rel)
            if any(n in low for n in IDFA_SDKS):
                idfa_sdks.append(rel)
        if p.suffix.lower() == ".md":
            for norm, msg in OBSOLETE_NORMS.items():
                if norm in text:
                    obsolete.append({"file": rel, "norm": norm, "note": msg})
    signals["ui"] = signals["ui"][:5]
    return {"signals": {k: v for k, v in signals.items() if v},
            "todo_legal": todo_legal,
            "arrepentimiento_in_code": arrepentimiento_in_code[:10],
            "consent_in_code": consent_in_code[:10],
            "telemetry_optout_in_code": optout_in_code[:10],
            "att_declared": att_declared[:10],
            "idfa_sdks": idfa_sdks[:10],
            "tracker_names": sorted(tracker_names),
            "obsolete_norms": obsolete}


WEB_STACK = {"nextjs", "nuxt", "astro", "static-html"}
WEB_DEPLOY = {"vercel", "netlify", "cloudflare", "cloudflare-workers"}
MOBILE_STACK = {"react-native", "expo", "capacitor", "flutter"}
DESKTOP_STACK = {"electron", "tauri"}


def detect_platforms(repo: Path, stack: list[str], signals: dict) -> list[str]:
    """Where the product runs on the user's side: web, mobile, desktop or cli. Several at once is valid."""
    s = set(stack)
    platforms = []
    mobile = bool(s & MOBILE_STACK) or ((repo / "android").is_dir() and (repo / "ios").is_dir())
    desktop = bool(s & DESKTOP_STACK)
    # Electron and React Native renderers ship Next, .tsx and .html too: in a native app only a
    # web deploy config proves there is also a public site.
    if s & WEB_DEPLOY or ((s & WEB_STACK or signals.get("ui")) and not (mobile or desktop)):
        platforms.append("web")
    if mobile:
        platforms.append("mobile")
    if desktop:
        platforms.append("desktop")
    return platforms or ["cli"]


def file_state(path: Path) -> str:
    if not path.exists():
        return "falta"
    if path.stat().st_size < MIN_CONTENT_BYTES and path.suffix == ".md":
        return "casi vacío"
    return "ok"


def find_one(repo: Path, *names: str) -> Path | None:
    for n in names:
        if (repo / n).exists():
            return repo / n
    return None


OSS_LICENSE = re.compile(r"MIT License|Apache License|GNU (?:AFFERO |LESSER )?GENERAL PUBLIC LICENSE"
                         r"|Mozilla Public License|BSD \d-Clause|Redistribution and use in source and binary"
                         r"|ISC License|This is free and unencumbered software", re.I)


def is_versioned(repo: Path) -> bool:
    """Publishes versions: a version field in a manifest, git tags, or a CHANGELOG already."""
    try:
        if json.loads(read(repo / "package.json") or "{}").get("version"):
            return True
    except json.JSONDecodeError:
        pass
    for manifest in ("pyproject.toml", "Cargo.toml"):
        if re.search(r'^\s*version\s*=\s*"', read(repo / manifest), re.M):
            return True
    tags = repo / ".git" / "refs" / "tags"
    if (tags.is_dir() and any(tags.iterdir())) or "refs/tags/" in read(repo / ".git" / "packed-refs"):
        return True
    return (repo / "CHANGELOG.md").exists()


def dir_state(path: Path) -> str:
    return "ok" if path.is_dir() and any(path.iterdir()) else "falta"


def check(repo: Path, args) -> dict:
    sc = scan(repo)
    lic = find_one(repo, "LICENSE.md", "LICENSE", "LICENSE.txt")
    # Public / open source: the user's answer wins; otherwise an OSI license text is the signal.
    public = args.public if args.public is not None else bool(lic and OSS_LICENSE.search(read(lic)))
    versioned = is_versioned(repo)
    # User answers win; detected signals are only a fallback guess.
    sells = args.sells_online if args.sells_online is not None else bool(sc["signals"].get("payments"))
    personal = args.personal_data if args.personal_data is not None else \
        any(sc["signals"].get(k) for k in ("auth", "forms", "trackers", "cookieless", "payments"))
    jur = (args.jurisdiction or "AR").upper()
    eu_users = args.eu_users if args.eu_users is not None else jur in {"EU", "UK", "GB"}
    stack = detect_stack(repo)
    platforms = detect_platforms(repo, stack, sc["signals"])
    trackers = sc["signals"].get("trackers", [])
    items = []

    def add(name, required, state, note=""):
        if not required and state == "falta":
            state = "no aplica"
        items.append({"file": name, "required": required, "state": state, "note": note})

    readme = repo / "README.md"
    add("README.md", True, file_state(readme))
    arch = find_one(repo, "ARCHITECTURE.md", "docs/ARCHITECTURE.md")
    add("ARCHITECTURE.md", True, file_state(arch) if arch else "falta",
        "en docs/" if arch and arch.parent.name == "docs" else "")
    adr_dir = repo / "docs" / "adr"
    add("docs/adr/0000-template.md", True, file_state(adr_dir / "0000-template.md"))
    first = sorted(adr_dir.glob("0001-*.md")) if adr_dir.is_dir() else []
    add("docs/adr/0001-*.md", True, file_state(first[0]) if first else "falta",
        first[0].name if first else "")

    design = repo / "DESIGN.md"
    if design.exists():
        add("DESIGN.md", args.ui_defined, file_state(design))
    else:
        readme_txt = read(readme).lower() if readme.exists() else ""
        noted = "design.md" in readme_txt or ("diseño" in readme_txt and "pendiente" in readme_txt)
        if args.ui_defined:
            add("DESIGN.md", True, "falta", "UI definida: corresponde DESIGN.md")
        else:
            add("DESIGN.md", False, "pendiente anotado" if noted else "pendiente sin anotar",
                "" if noted else "Anotar en README que el diseño UX/UI está pendiente")

    # The product's north is never inferred from code: required only once the user says it is defined.
    roadmap = repo / "ROADMAP.md"
    plans = sorted(p.relative_to(repo).as_posix() for p in (repo / "docs" / "specs").glob("*/plan.md")) \
        if (repo / "docs" / "specs").is_dir() else []
    plan_note = f"enlazar {', '.join(plans[:3])}" if plans else ""
    if roadmap.exists():
        add("ROADMAP.md", True, file_state(roadmap), plan_note)
    elif args.roadmap_defined:
        add("ROADMAP.md", True, "falta", "; ".join(filter(None, ["Norte definido: corresponde ROADMAP.md", plan_note])))
    else:
        readme_txt = read(readme).lower() if readme.exists() else ""
        noted = "roadmap.md" in readme_txt or ("roadmap" in readme_txt and "pendiente" in readme_txt)
        add("ROADMAP.md", False, "pendiente anotado" if noted else "pendiente sin anotar",
            "" if noted else "Anotar en README que el roadmap está pendiente (norte no definido)")

    add("PRIVACY.md", personal, file_state(repo / "PRIVACY.md"),
        "maneja datos personales" if personal else "")
    add("TERMS.md", sells or personal, file_state(repo / "TERMS.md"),
        "vende online" if sells else "")
    if sells and jur == "AR":
        found = sc["arrepentimiento_in_code"]
        add("Botón de arrepentimiento (UI)", True, "ok" if found else "falta",
            ", ".join(found[:3]) if found else "Disp. SSDCyLC 954/2025: visible en primer acceso, sin registro, respuesta 24 h con código")

    # Cookies and tracking: what is required depends on where the product runs.
    seen = ", ".join(sc["tracker_names"][:4]) + (f" (en {', '.join(trackers[:2])})" if trackers else "")
    web_tracking = "web" in platforms and bool(trackers)
    add("COOKIES.md", web_tracking, file_state(repo / "COOKIES.md"), seen if web_tracking else "")
    if "web" in platforms:
        consent = sc["consent_in_code"]
        if not trackers:
            add("Consentimiento de cookies (UI)", False, "falta")
        elif consent:
            add("Consentimiento de cookies (UI)", eu_users, "ok", ", ".join(consent[:3]))
        elif eu_users:
            add("Consentimiento de cookies (UI)", True, "falta",
                "usuarios en UE/UK: consentimiento previo, rechazar tan fácil como aceptar")
        else:
            add("Consentimiento de cookies (UI)", False, "recomendado",
                "obligatorio solo con usuarios en UE/UK (--eu-users)")
    native = [p for p in platforms if p != "web"]
    if trackers and native:
        priv = repo / "PRIVACY.md"
        if not priv.exists():
            state = "falta"
        else:
            state = "ok" if PRIVACY_TRACKING.search(read(priv)) else "incompleto"
        add("PRIVACY.md § rastreo", True, state,
            f"{seen}: sección de rastreo/telemetría con SDK, dato, finalidad y cómo desactivarlo")
    if "mobile" in platforms:
        android_only = (repo / "android").is_dir() and not (repo / "ios").is_dir() \
            and not {"expo", "react-native", "capacitor", "flutter"} & set(stack)
        needs_att = bool(sc["idfa_sdks"]) and not android_only
        att = sc["att_declared"]
        add("ATT (iOS)", needs_att, "ok" if att else "falta",
            ", ".join(att[:3]) if att else
            ("NSUserTrackingUsageDescription en Info.plist (o ios.infoPlist en app.json)" if needs_att else ""))
    if trackers and ({"desktop", "cli"} & set(platforms)):
        optout = sc["telemetry_optout_in_code"]
        add("Opt-out de telemetría", True, "ok" if optout else "falta",
            ", ".join(optout[:3]) if optout else "flag o env var (p. ej. DO_NOT_TRACK) para desactivarla")
    add("SECURITY.md", True, file_state(repo / "SECURITY.md"))
    lic = find_one(repo, "LICENSE.md", "LICENSE", "LICENSE.txt")
    add("LICENSE.md", True, file_state(lic) if lic else "falta",
        lic.name if lic and lic.name != "LICENSE.md" else "")
    gi = repo / ".gitignore"
    gi_state = "ok" if gi.exists() else "falta"
    gi_note = ""
    if gi.exists() and not re.search(r"^\.env\b", read(gi), re.M):
        gi_state, gi_note = "incompleto", ".env no está ignorado"
    add(".gitignore", True, gi_state, gi_note)
    ga = repo / ".gitattributes"
    ga_state = "falta"
    if ga.exists():
        ga_state = "ok" if re.search(r"^\*\s+text=auto\s+eol=lf", read(ga), re.M) else "incompleto"
    add(".gitattributes", True, ga_state, "" if ga_state != "incompleto" else "falta '* text=auto eol=lf'")
    add(".editorconfig", True, "ok" if (repo / ".editorconfig").exists() else "falta")

    # Community files: only for public / open source repos.
    note = "repo público / open source" if public else ""
    add("CONTRIBUTING.md", public, file_state(find_one(repo, "CONTRIBUTING.md", ".github/CONTRIBUTING.md", "docs/CONTRIBUTING.md") or repo / "CONTRIBUTING.md"), note)
    add("CODE_OF_CONDUCT.md", public, file_state(find_one(repo, "CODE_OF_CONDUCT.md", ".github/CODE_OF_CONDUCT.md", "docs/CODE_OF_CONDUCT.md") or repo / "CODE_OF_CONDUCT.md"), note)
    pr = find_one(repo, ".github/PULL_REQUEST_TEMPLATE.md", ".github/pull_request_template.md",
                  "PULL_REQUEST_TEMPLATE.md", "docs/PULL_REQUEST_TEMPLATE.md")
    add(".github/PULL_REQUEST_TEMPLATE.md", public, "ok" if pr else "falta", note)
    add(".github/ISSUE_TEMPLATE/", public, dir_state(repo / ".github" / "ISSUE_TEMPLATE"), note)
    add("CHANGELOG.md", versioned, file_state(repo / "CHANGELOG.md"), "publica versiones" if versioned else "")

    missing = [i for i in items if i["required"] and i["state"] not in ("ok", "pendiente anotado")]
    return {"repo": str(repo.resolve()), "stack": stack, "jurisdiction": jur,
            "assumed": {"sells_online": sells, "personal_data": personal, "ui_defined": args.ui_defined,
                        "roadmap_defined": args.roadmap_defined,
                        "public": public, "versioned": versioned,
                        "platforms": platforms, "eu_users": eu_users, "trackers": sc["tracker_names"]},
            "items": items, "missing_count": len(missing), **sc}


def print_table(r: dict) -> None:
    print(f"Repo: {r['repo']}")
    print(f"Stack detectado: {', '.join(r['stack']) or 'no detectado'}")
    a = r["assumed"]
    print(f"Supuestos: vende online={a['sells_online']} · datos personales={a['personal_data']} · "
          f"UI definida={a['ui_defined']} · norte definido={a['roadmap_defined']} · "
          f"jurisdicción={r['jurisdiction']} · usuarios UE/UK={a['eu_users']}")
    print(f"Plataformas: {', '.join(a['platforms'])} · rastreadores: {', '.join(a['trackers'][:3]) or 'ninguno'}")
    print()
    w = max(len(i["file"]) for i in r["items"]) + 2
    print(f"{'Archivo'.ljust(w)}{'Req.'.ljust(6)}{'Estado'.ljust(22)}Nota")
    print("-" * (w + 60))
    for i in r["items"]:
        req = "sí" if i["required"] else "no"
        print(f"{i['file'].ljust(w)}{req.ljust(6)}{i['state'].ljust(22)}{i['note']}")
    print()
    if r["todo_legal"]:
        total = sum(r["todo_legal"].values())
        print(f"TODO-LEGAL pendientes: {total}")
        for f, n in r["todo_legal"].items():
            print(f"  {f}: {n}")
    if r["obsolete_norms"]:
        print("Normas derogadas citadas:")
        for o in r["obsolete_norms"]:
            print(f"  {o['file']}: {o['note']}")
    print(f"\nFaltan {r['missing_count']} elemento(s) requerido(s)." if r["missing_count"]
          else "\nBaseline completo.")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("repo", nargs="?", default=".")
    ap.add_argument("--json", action="store_true", help="salida JSON")
    ap.add_argument("--sells-online", action=argparse.BooleanOptionalAction, default=None,
                    help="override detection (--no-sells-online to deny)")
    ap.add_argument("--personal-data", action=argparse.BooleanOptionalAction, default=None,
                    help="override detection (--no-personal-data to deny)")
    ap.add_argument("--ui-defined", action=argparse.BooleanOptionalAction, default=False)
    ap.add_argument("--roadmap-defined", action=argparse.BooleanOptionalAction, default=False,
                    help="el norte del producto esta definido: ROADMAP.md pasa a ser requerido")
    ap.add_argument("--public", action=argparse.BooleanOptionalAction, default=None,
                    help="repo publico / open source (--no-public to deny); default: OSI license detected")
    ap.add_argument("--eu-users", action=argparse.BooleanOptionalAction, default=None,
                    help="hay usuarios en UE/UK: el consentimiento de cookies pasa a ser requerido; "
                         "default: solo con --jurisdiction EU o UK")
    ap.add_argument("--jurisdiction", default="AR")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    repo = Path(args.repo)
    if not repo.is_dir():
        print(f"No existe el directorio: {repo}", file=sys.stderr)
        return 2
    r = check(repo, args)
    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print_table(r)
    return 1 if r["missing_count"] else 0


if __name__ == "__main__":
    sys.exit(main())
```
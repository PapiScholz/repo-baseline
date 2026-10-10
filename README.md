# repo-baseline

**Que todo repo nazca con su documentación mínima, escrita para ese proyecto.**

[English below](#english)

Skill para Claude Code y claude.ai. Deja cualquier repo, sitio o software con su set básico de documentación. Las plantillas no quedan con `TODO: describir el proyecto`: los documentos salen de lo que el propio repo dice de sí mismo.

| Archivo | Cuándo |
|---|---|
| `README.md` y READMEs por carpeta con reglas propias | Siempre |
| `ARCHITECTURE.md` | Siempre |
| `docs/adr/0000-template.md` + `0001-<decisión>.md` | Siempre |
| `DESIGN.md` (formato google-labs-code/design.md) | Si el diseño UX/UI está definido |
| `PRIVACY.md` / `TERMS.md` | Si maneja datos personales / si hay usuarios finales o venta |
| Botón de arrepentimiento | Si vende online en Argentina |
| `SECURITY.md`, `LICENSE.md`, `.gitignore`, `.gitattributes` | Siempre |

## Cómo trabaja

1. **Detecta antes de preguntar.** Corre `check_baseline.py`, incluido en la skill (Apéndice D), y lee `package.json`, las configs de deploy, el CI y el README existente. Saca de ahí el stack, lo que falta y señales como pagos, auth o datos personales.
2. **Pregunta solo lo que no pudo deducir**, en un único formulario: titular del código, jurisdicción (Argentina por defecto, siempre confirmada), si vende online, si maneja datos personales y si el diseño está definido.
3. **Verifica la normativa vigente** antes de escribir legales. Lo que falte queda marcado `TODO-LEGAL`.
4. **Redacta sin inventar decisiones.** Lo que propone sin confirmar queda marcado `(sugerido — confirmar)`.
5. **Nunca sobrescribe.** Si un archivo existe, propone un diff.
6. **Verifica** corriendo el check de nuevo y **cierra con una tabla de estado** más la lista de `TODO-LEGAL`, para pasársela al contador o al cliente.

No hace operaciones de git, no instala dependencias ni toca el código de la app.

## Instalar

**Claude Code**, con el CLI de [skills](https://skills.sh):

```bash
npx skills add PapiScholz/repo-baseline -g
```

**A mano:** copiá `SKILL.md` a `~/.claude/skills/repo-baseline/SKILL.md`.

**claude.ai:** Configuración → Capacidades → Skills → subir `SKILL.md`.

Después: *"armá el baseline de este repo"*, o invocá `/repo-baseline`.

## Tests

```bash
python -m unittest discover tests
```

La skill le pide al agente que copie `check_baseline.py` tal cual desde el Apéndice D. Si ese bloque se rompe, la skill falla en silencio. Por eso los tests lo extraen de `SKILL.md` y lo corren contra repos de prueba. Lo verifiqué metiendo un error de sintaxis en el bloque: los 4 tests dieron rojo.

## Licencia

MIT

---

## English

A Claude Code / claude.ai skill that gives any repository its minimum documentation, written for that project:

- README, ARCHITECTURE, ADRs, DESIGN when the UI is defined, SECURITY, LICENSE, `.gitignore` and `.gitattributes`;
- privacy and terms where they apply. Argentina is the default jurisdiction, always confirmed; a generic template covers others.

It reads the repo before asking anything, asks the rest in a single form, never overwrites existing files (it proposes diffs) and ends with a status table. The skill text is in Spanish.

```bash
npx skills add PapiScholz/repo-baseline -g
```

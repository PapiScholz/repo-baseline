#!/usr/bin/env python3
"""Compara el SKILL.md de este repo (la fuente de verdad) con las copias instaladas.

Busca repo-baseline/SKILL.md bajo el directorio de skills de Claude Code
($CLAUDE_CONFIG_DIR o ~/.claude), incluidas las sincronizadas desde claude.ai
(skills/synced/*/repo-baseline). Sale con 1 si alguna copia difiere.

  python tools/drift.py
"""
import hashlib
import os
import sys
from pathlib import Path

REPO_SKILL = Path(__file__).resolve().parents[1] / "SKILL.md"


def digest(p: Path) -> str:
    return hashlib.sha256(p.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def installed_copies(base: Path):
    skills = base / "skills"
    if not skills.is_dir():
        return []
    found = [p for p in skills.glob("repo-baseline/SKILL.md")]
    found += [p for p in skills.glob("synced/*/repo-baseline/SKILL.md")]
    return found


def main() -> int:
    # La consola de Windows por defecto es cp1252: sin esto, imprimir "→" o acentos crashea.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    base = Path(os.environ.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude")
    ref = digest(REPO_SKILL)
    copies = installed_copies(base)
    if not copies:
        print("No hay copias instaladas de repo-baseline.")
        return 0
    drift = False
    for p in copies:
        same = digest(p) == ref
        drift |= not same
        print(f"{'igual    ' if same else 'DISTINTA '} {p}")
    if drift:
        print("\nEl repo es la fuente de verdad. Para alinear una copia:")
        print("  - local:     npx skills add PapiScholz/repo-baseline -g   (o copiá SKILL.md encima)")
        print("  - claude.ai: Configuración → Capacidades → Skills → reemplazar con el SKILL.md del repo")
        print("Si la copia instalada tiene cambios que querés conservar, pasalos primero al repo.")
    return 1 if drift else 0


if __name__ == "__main__":
    sys.exit(main())

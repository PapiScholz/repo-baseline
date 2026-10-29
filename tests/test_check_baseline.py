"""Extrae check_baseline.py del Apéndice D de SKILL.md y lo corre contra repos de prueba.

La skill le pide al agente que copie ese script "tal cual": si el bloque deja de compilar o de detectar,
la skill entera falla en silencio. Run: python -m unittest discover tests
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def extract_script() -> str:
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    section = text.split("## Apéndice D", 1)[1]
    m = re.search(r"```python\n(.*?)\n```", section, re.S)
    assert m, "no hay bloque ```python en el Apéndice D"
    return m.group(1)


class TestCheckBaseline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp())
        cls.script = cls.tmp / "check_baseline.py"
        cls.script.write_text(extract_script(), encoding="utf-8")

    def run_check(self, repo: Path, *flags):
        r = subprocess.run([sys.executable, "-X", "utf8", str(self.script), str(repo), "--json", *flags],
                           capture_output=True, text=True, encoding="utf-8")
        self.assertIn(r.returncode, (0, 1), r.stderr)
        return json.loads(r.stdout)

    def test_script_compiles(self):
        compile(self.script.read_text(encoding="utf-8"), "check_baseline.py", "exec")

    def test_empty_repo_reports_core_files_missing(self):
        repo = self.tmp / "empty"
        repo.mkdir()
        out = json.dumps(self.run_check(repo))
        for f in ("README.md", "ARCHITECTURE.md", "SECURITY.md", ".gitignore"):
            self.assertIn(f, out)

    @staticmethod
    def states(report):
        return {i["file"]: i["state"] for i in report["items"]}

    def test_states_change_from_missing_to_thin_to_complete(self):
        empty = self.tmp / "e"
        empty.mkdir()
        thin = self.tmp / "thin"
        thin.mkdir()
        (thin / "README.md").write_text("# x\n", encoding="utf-8")
        full = self.tmp / "full"
        full.mkdir()
        (full / "README.md").write_text("# Proyecto\n\n" + "Qué es, cómo se corre y cómo se despliega. " * 40, encoding="utf-8")
        (full / ".gitignore").write_text("node_modules/\n.env\n.env.*\n", encoding="utf-8")
        (full / ".gitattributes").write_text("* text=auto eol=lf\n", encoding="utf-8")
        s_empty, s_thin, s_full = (self.states(self.run_check(r)) for r in (empty, thin, full))
        self.assertNotEqual(s_empty["README.md"], s_thin["README.md"])
        self.assertEqual(s_thin["README.md"], "casi vacío")
        self.assertNotIn(s_full["README.md"], (s_empty["README.md"], "casi vacío"))
        self.assertNotEqual(s_full[".gitignore"], "incompleto")
        self.assertNotEqual(s_full[".gitattributes"], "incompleto")

    MIT = "MIT License\n\nCopyright (c) 2026 x\n\nPermission is hereby granted, free of charge, " * 3

    def test_open_source_repo_requires_community_files(self):
        repo = self.tmp / "oss"
        repo.mkdir()
        (repo / "LICENSE").write_text(self.MIT, encoding="utf-8")
        report = self.run_check(repo)
        s = self.states(report)
        self.assertTrue(report["assumed"]["public"])
        for f in ("CONTRIBUTING.md", "CODE_OF_CONDUCT.md", ".github/PULL_REQUEST_TEMPLATE.md",
                  ".github/ISSUE_TEMPLATE/"):
            self.assertEqual(s.get(f), "falta", (f, s))
        self.assertEqual(s.get(".editorconfig"), "falta")

    def test_private_repo_does_not_require_community_files(self):
        repo = self.tmp / "priv"
        repo.mkdir()
        s = self.states(self.run_check(repo, "--no-public"))
        for f in ("CONTRIBUTING.md", "CODE_OF_CONDUCT.md"):
            self.assertEqual(s.get(f), "no aplica", (f, s))
        self.assertEqual(s.get(".editorconfig"), "falta")

    def test_changelog_required_only_when_versioned(self):
        plain = self.tmp / "nover"
        plain.mkdir()
        versioned = self.tmp / "ver"
        versioned.mkdir()
        (versioned / "package.json").write_text(json.dumps({"name": "x", "version": "1.2.0"}), encoding="utf-8")
        self.assertEqual(self.states(self.run_check(plain, "--no-public")).get("CHANGELOG.md"), "no aplica")
        self.assertEqual(self.states(self.run_check(versioned, "--no-public")).get("CHANGELOG.md"), "falta")

    def test_roadmap_pending_until_north_defined(self):
        bare = self.tmp / "rm_bare"
        bare.mkdir()
        report = self.run_check(bare, "--no-public")
        self.assertEqual(self.states(report).get("ROADMAP.md"), "pendiente sin anotar")
        noted = self.tmp / "rm_noted"
        noted.mkdir()
        (noted / "README.md").write_text("# x\n\nRoadmap: pendiente, el norte no está definido.\n", encoding="utf-8")
        self.assertEqual(self.states(self.run_check(noted, "--no-public")).get("ROADMAP.md"), "pendiente anotado")
        # Pending (noted or not) never counts as missing: only the north being defined makes it required.
        defined = self.run_check(bare, "--no-public", "--roadmap-defined")
        self.assertEqual(defined["missing_count"], report["missing_count"] + 1)

    def test_roadmap_missing_when_north_defined(self):
        repo = self.tmp / "rm_def"
        repo.mkdir()
        self.assertEqual(self.states(self.run_check(repo, "--no-public", "--roadmap-defined")).get("ROADMAP.md"), "falta")
        (repo / "ROADMAP.md").write_text("# Roadmap\n\n## Norte\n" + "Qué es el producto terminado. " * 20, encoding="utf-8")
        self.assertEqual(self.states(self.run_check(repo, "--no-public", "--roadmap-defined")).get("ROADMAP.md"), "ok")
        self.assertEqual(self.states(self.run_check(repo, "--no-public")).get("ROADMAP.md"), "ok")

    def test_roadmap_note_links_staged_plan(self):
        repo = self.tmp / "rm_plan"
        (repo / "docs" / "specs" / "c1").mkdir(parents=True)
        (repo / "docs" / "specs" / "c1" / "plan.md").write_text("# Plan\n", encoding="utf-8")
        item = next(i for i in self.run_check(repo, "--no-public", "--roadmap-defined")["items"]
                    if i["file"] == "ROADMAP.md")
        self.assertIn("docs/specs/c1/plan.md", item["note"])

    def test_github_actions_checkout_is_not_a_payment_signal(self):
        repo = self.tmp / "ci"
        (repo / ".github" / "workflows").mkdir(parents=True)
        (repo / ".github" / "workflows" / "lint.yml").write_text(
            "jobs:\n  a:\n    steps:\n      - uses: actions/checkout@v4\n", encoding="utf-8")
        report = self.run_check(repo)
        self.assertNotIn("payments", report["signals"], report["signals"])
        self.assertFalse(report["assumed"]["sells_online"])

    def test_architecture_under_docs_counts(self):
        repo = self.tmp / "arch"
        (repo / "docs").mkdir(parents=True)
        (repo / "docs" / "ARCHITECTURE.md").write_text("# Arquitectura\n\n" + "Componentes y flujo. " * 30, encoding="utf-8")
        s = self.states(self.run_check(repo))
        self.assertEqual(s["ARCHITECTURE.md"], "ok", s)

    def test_detects_node_stack(self):
        repo = self.tmp / "node"
        repo.mkdir()
        (repo / "package.json").write_text(json.dumps({"name": "x", "dependencies": {"next": "15", "mercadopago": "2"}}), encoding="utf-8")
        out = json.dumps(self.run_check(repo)).lower()
        self.assertTrue("node" in out or "next" in out, out[:400])


class TestDrift(unittest.TestCase):
    def run_drift(self, base: Path):
        env = {**os.environ, "CLAUDE_CONFIG_DIR": str(base)}
        return subprocess.run([sys.executable, "-X", "utf8", str(ROOT / "tools" / "drift.py")],
                              capture_output=True, text=True, encoding="utf-8", env=env)

    def test_detects_identical_and_drifted_copies(self):
        base = Path(tempfile.mkdtemp())
        synced = base / "skills" / "synced" / "abc" / "repo-baseline"
        synced.mkdir(parents=True)
        (synced / "SKILL.md").write_bytes((ROOT / "SKILL.md").read_bytes())
        r = self.run_drift(base)
        self.assertEqual(r.returncode, 0, r.stdout)
        (synced / "SKILL.md").write_text("editado en claude.ai", encoding="utf-8")
        r = self.run_drift(base)
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("DISTINTA", r.stdout)

    def test_drift_report_survives_a_cp1252_console(self):
        # La consola de Windows por defecto no es UTF-8: el reporte no puede crashear al imprimir.
        base = Path(tempfile.mkdtemp())
        synced = base / "skills" / "synced" / "abc" / "repo-baseline"
        synced.mkdir(parents=True)
        (synced / "SKILL.md").write_text("editado en claude.ai", encoding="utf-8")
        env = {**os.environ, "CLAUDE_CONFIG_DIR": str(base), "PYTHONIOENCODING": "cp1252", "PYTHONUTF8": "0"}
        r = subprocess.run([sys.executable, str(ROOT / "tools" / "drift.py")],
                           capture_output=True, env=env)
        self.assertNotIn(b"UnicodeEncodeError", r.stderr, r.stderr[-300:])
        self.assertEqual(r.returncode, 1, r.stderr[-300:])


if __name__ == "__main__":
    unittest.main()

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


if __name__ == "__main__":
    unittest.main()

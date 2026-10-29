"""Repository-specific structural checks, not full host schema validation."""

import json
import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

# Skills per plugin, their eval files and a German routing cue each description must carry.
PLUGINS = {
    "codemetr-csharp": {
        "skills": {"analyze", "guard"},
        "evals": "evals/evals.json",
        "queries": "evals/trigger-queries.json",
        "cue": "Code-Metriken",
    },
    "codemetr-csharp-cover": {
        "skills": {"coverage", "coverage-guard"},
        "evals": "evals/codemetr-csharp-cover.evals.json",
        "queries": "evals/codemetr-csharp-cover.trigger-queries.json",
        "cue": "Testabdeckung",
    },
}


def load(relative):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class PackagingTests(unittest.TestCase):
    def test_marketplaces_point_to_same_plugins(self):
        claude = load(".claude-plugin/marketplace.json")
        codex = load(".agents/plugins/marketplace.json")
        self.assertEqual(claude["name"], codex["name"])
        self.assertTrue(claude["owner"]["name"])
        left = {p["name"]: p["source"] for p in claude["plugins"]}
        right = {p["name"]: p["source"]["path"] for p in codex["plugins"]}
        self.assertEqual(left, right)
        self.assertEqual(len(left), len(claude["plugins"]))
        self.assertEqual(len(right), len(codex["plugins"]))
        for entry in codex["plugins"]:
            self.assertEqual(entry["source"]["source"], "local")
        for name, source in left.items():
            self.assertTrue(source.startswith("./"))
            plugin = (ROOT / source).resolve()
            self.assertTrue(plugin.is_relative_to(ROOT))
            self.assertTrue(plugin.is_dir())
            manifests = [
                json.loads((plugin / host / "plugin.json").read_text())
                for host in (".claude-plugin", ".codex-plugin")
            ]
            for manifest in manifests:
                self.assertEqual(manifest["name"], name)
                self.assertEqual(manifest["skills"], "./skills/")
                self.assertRegex(manifest["version"], r"^\d+\.\d+\.\d+$")
            self.assertEqual(manifests[0]["version"], manifests[1]["version"])
            self.assertEqual(manifests[0]["description"], manifests[1]["description"])

    def test_skills_and_local_references(self):
        skills = list(ROOT.glob("plugins/*/skills/*/SKILL.md"))
        self.assertEqual({p.parent.parent.parent.name for p in skills}, set(PLUGINS))
        for plugin, spec in PLUGINS.items():
            self.assertEqual({p.parent.name for p in skills if p.parents[2].name == plugin}, spec["skills"])
        names = [p.parent.name for p in skills]
        self.assertEqual(len(names), len(set(names)), "skill names must be unique across plugins")
        for path in skills:
            text = path.read_text(encoding="utf-8")
            self.assertTrue(text.startswith("---\n"), path)
            frontmatter, body = text[4:].split("\n---\n", 1)
            fields = dict(line.split(": ", 1) for line in frontmatter.splitlines())
            self.assertEqual(fields["name"], path.parent.name)
            self.assertGreater(len(fields["description"]), 40)
            self.assertLess(len(text.splitlines()), 500)
            self.assertIn("compatibility", fields)
            self.assertTrue(body.strip())
            for target in re.findall(r"\]\(([^)]+)\)", text):
                resolved = (path.parent / target).resolve()
                self.assertTrue(resolved.is_relative_to(path.parents[2]), target)
                self.assertTrue(resolved.is_file(), target)

    def test_cover_skills_explain_drops_only_from_evidence(self):
        for skill in ("coverage", "coverage-guard"):
            text = (ROOT / "plugins/codemetr-csharp-cover/skills" / skill / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("skippedTestsIncreased", text, skill)
            self.assertIn("unverified", text, skill)

    def test_eval_prompts_are_unique(self):
        for plugin, spec in PLUGINS.items():
            document = load(spec["evals"])
            self.assertEqual(document["skill_name"], plugin)
            evals = document["evals"]
            self.assertGreaterEqual(len(evals), 3)
            self.assertEqual(len(evals), len({e["id"] for e in evals}))
            for entry in evals:
                self.assertTrue(entry["prompt"])
                self.assertTrue(entry["expected_output"])

    def test_implicit_routing_metadata_and_queries(self):
        for plugin, spec in PLUGINS.items():
            for skill in spec["skills"]:
                text = (ROOT / "plugins" / plugin / "skills" / skill / "SKILL.md").read_text(encoding="utf-8")
                frontmatter = text.split("---", 2)[1]
                self.assertNotIn("disable-model-invocation: true", frontmatter)
                self.assertIn("The user need not name Codemetr", frontmatter)
                self.assertIn(spec["cue"], frontmatter)
            queries = load(spec["queries"])
            self.assertEqual(len(queries), len({q["query"] for q in queries}))
            for skill in spec["skills"]:
                entries = [q for q in queries if q["skill"] == skill]
                self.assertTrue(any(q["should_trigger"] for q in entries), skill)
                self.assertTrue(any(not q["should_trigger"] for q in entries), skill)

    def test_no_obvious_credentials_or_private_paths(self):
        # Inspect tracked and non-ignored new files; report file names, not values.
        output = subprocess.check_output(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
            cwd=ROOT,
        )
        patterns = [
            r"gh[pousr]_[A-Za-z0-9]{20,}",
            r"github_pat_[A-Za-z0-9_]{20,}",
            r"-----BEGIN (?:[A-Z ]+)?PRIVATE KEY-----",
            r"https?://[^\s/]+:[^\s/]+@",
            r"C:\\Users\\[^\\\s]+",
            r"/(?:Users|home)/[A-Za-z0-9_.-]+/",
        ]
        for name in set(output.decode("utf-8").split("\0")) - {""}:
            path = ROOT / name
            with self.subTest(file=name):
                self.assertNotIn(path.suffix.lower(), {".pfx", ".p12", ".key", ".pem"})
                self.assertFalse(path.name == ".env" or path.name.startswith(".env."))
                try:
                    text = path.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    continue
                for pattern in patterns:
                    self.assertIsNone(re.search(pattern, text), name)


if __name__ == "__main__":
    unittest.main()

"""Behavioral checks for workspace safety, stage gates, and manifest leakage."""

import csv
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

import yaml

SKILL = Path(__file__).resolve().parents[1]


class HelperTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="cv-skill-test-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / "nested" / "research"
        self.run_script("init_research.py", "--root", self.root)

    def run_script(self, name, *args, code=0):
        result = subprocess.run(
            [sys.executable, "-B", str(SKILL / "scripts" / name), *map(str, args)],
            cwd=self.base, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        return result.stdout

    def state(self):
        text = (self.root / "STATE.md").read_text()
        return yaml.safe_load(re.search(r"```yaml\n(.*?)\n```", text, re.S).group(1))

    def save_state(self, state):
        (self.root / "STATE.md").write_text("# Research State\n\n```yaml\n" + yaml.safe_dump(state) + "```\n")

    def validate(self, strict=False, code=0):
        args = ["--root", self.root] + (["--strict"] if strict else [])
        return self.run_script("validate_state.py", *args, code=code)

    def pass_gates(self, state, names):
        evidence = self.root / "evidence.md"
        evidence.write_text("[MEASURED] Synthetic evidence for a helper test only.\n")
        for name in names:
            state["gates"][name] = "PASS"
            state["gate_evidence"][name] = ["evidence.md"]
        state["acceptance"]["contract_id"] = "contract-v1"

    def manifest(self, rows, fields=None):
        path = self.base / "manifest.csv"
        fields = fields or ["sample_id", "split", "path", "group_id", "sha256", "label_path", "condition"]
        with path.open("w", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
        return path

    def audit(self, rows, *args, code=0):
        return json.loads(self.run_script("audit_manifest.py", self.manifest(rows), *args, code=code))

    def test_fresh_workspace_valid_at_intake(self):
        self.validate(strict=True)
        self.assertIn("Constraints and Budget", (self.root / "problem/constraints.md").read_text())
        self.assertTrue((self.root / "problem/acceptance.md").is_file())

    def test_initialization_preserves_existing_bytes_and_mtime(self):
        state = self.root / "STATE.md"
        state.write_text("User-owned record with blank created:\n")
        before = state.stat().st_mtime_ns
        self.run_script("init_research.py", "--root", self.root)
        self.assertEqual(state.read_text(), "User-owned record with blank created:\n")
        self.assertEqual(before, state.stat().st_mtime_ns)

    def test_invalid_yaml_and_duplicate_keys_fail_cleanly(self):
        for content in ("no YAML here", "```yaml\nproject: [\n```", "```yaml\nproject: {}\nproject: {}\n```"):
            with self.subTest(content=content):
                (self.root / "STATE.md").write_text(content)
                self.validate(code=1)

    def test_invalid_types_and_enums_fail_cleanly(self):
        original = self.state()
        for key, value in (("research_stage", []), ("project", []), ("gates", "PASS"),
                           ("gate_notes", []), ("acceptance", None), ("schema_version", True)):
            with self.subTest(key=key):
                state = dict(original)
                state[key] = value
                self.save_state(state)
                self.validate(strict=True, code=1)

    def test_invalid_nested_status_types_fail_cleanly(self):
        original = self.state()
        for section, key in (("project", "status"), ("acceptance", "status"), ("gates", "data")):
            for value in ([], {}, True, "TYPO"):
                with self.subTest(section=section, value=value):
                    state = json.loads(json.dumps(original, default=str))
                    state[section][key] = value
                    self.save_state(state)
                    self.validate(strict=True, code=1)

    def test_legacy_state_is_readable_without_silent_migration(self):
        state = {"project": {"status": "INTAKE"}, "research_stage": "INTAKE",
                 "next_action": None, "best_checkpoint": None}
        self.save_state(state)
        before = (self.root / "STATE.md").read_bytes()
        self.assertIn("Legacy", self.validate())
        self.validate(strict=True, code=1)
        self.assertEqual(before, (self.root / "STATE.md").read_bytes())

    def test_pass_claim_requires_evidence(self):
        state = self.state()
        state["gates"]["data"] = "PASS"
        self.save_state(state)
        self.assertIn("no gate_evidence", self.validate(code=1))
        state["gate_evidence"]["data"] = ["missing.md"]
        self.save_state(state)
        self.validate()
        self.assertIn("does not exist", self.validate(strict=True, code=1))

    def test_strict_training_blocks_missing_gates_but_allows_first_baseline(self):
        state = self.state()
        state["research_stage"] = "TRAINING"
        self.save_state(state)
        self.validate(strict=True, code=1)
        self.pass_gates(state, ("requirements", "feasibility", "data"))
        state["budget"]["scope"] = "Authorized small baseline run; stop after the fixed budget."
        self.save_state(state)
        self.validate(strict=True)

    def test_evaluating_supplied_model_does_not_require_baseline_training(self):
        state = self.state()
        state["research_stage"] = "EVALUATION"
        self.pass_gates(state, ("requirements", "data"))
        self.save_state(state)
        self.validate(strict=True)

    def test_unmet_goal_cannot_be_marked_complete(self):
        state = self.state()
        state["project"]["status"] = "COMPLETED"
        state["project"]["outcome"] = "ACCEPTED"
        self.save_state(state)
        self.validate(strict=True, code=1)

    def test_budget_exhaustion_is_valid_stopped_outcome(self):
        state = self.state()
        state["project"].update(status="STOPPED", outcome="BUDGET_EXHAUSTED")
        state["research_stage"] = "TRAINING"
        state["budget"]["stop_reason"] = "Authorized budget consumed before reaching the target."
        self.save_state(state)
        self.validate(strict=True)

    def test_completed_model_requires_artifacts_and_all_gates(self):
        state = self.state()
        self.pass_gates(state, state["gates"])
        state["project"].update(status="COMPLETED", outcome="ACCEPTED")
        state["research_stage"] = "DELIVERY"
        state["acceptance"].update(status="ACCEPTED", evidence_path="evidence.md")
        state["artifacts"]["delivery"] = "evidence.md"
        state["best_checkpoint"] = "weights.bin"
        (self.root / "weights.bin").write_bytes(b"fixture, not real model weights")
        state["reproduction"] = {key: "test-fixture" for key in state["reproduction"]}
        self.save_state(state)
        self.validate(strict=True)
        state["gates"]["data"] = "NOT_APPLICABLE"
        state["gate_notes"]["data"] = "attempt to bypass data acceptance"
        self.save_state(state)
        self.validate(strict=True, code=1)

    def test_clean_manifest_and_slice_support(self):
        (self.base / "a.bin").write_bytes(b"one")
        (self.base / "b.bin").write_bytes(b"two")
        result = self.audit([
            {"sample_id": "a", "split": "train", "path": "a.bin", "group_id": "g1", "condition": "x"},
            {"sample_id": "b", "split": "test", "path": "b.bin", "group_id": "g2", "condition": "x"},
        ], "--hash-files", "--require-groups", "--slice-column", "condition")
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["warnings"], [])
        self.assertEqual(result["slice_counts"]["condition"]["test"]["x"], 1)
        self.assertIn("annotation semantics/geometry", result["checks_not_performed"])

    def test_group_and_declared_hash_leakage(self):
        result = self.audit([
            {"sample_id": "a", "split": "train", "path": "a", "group_id": "g", "sha256": "a" * 64},
            {"sample_id": "b", "split": "val", "path": "b", "group_id": "g", "sha256": "a" * 64},
        ], code=1)
        self.assertTrue(any("group crosses" in error for error in result["errors"]))
        self.assertTrue(any("hash crosses" in error for error in result["errors"]))

    def test_duplicate_paths_are_canonicalized(self):
        result = self.audit([
            {"sample_id": "a", "split": "train", "path": "folder/../a.bin"},
            {"sample_id": "b", "split": "test", "path": "a.bin"},
        ], code=1)
        self.assertTrue(any("duplicate path" in error for error in result["errors"]))

    def test_computed_hash_leakage_and_mismatch(self):
        (self.base / "a").write_bytes(b"same")
        (self.base / "b").write_bytes(b"same")
        result = self.audit([
            {"sample_id": "a", "split": "train", "path": "a", "sha256": "0" * 64},
            {"sample_id": "b", "split": "test", "path": "b"},
        ], "--hash-files", code=1)
        self.assertTrue(any("mismatch" in error for error in result["errors"]))
        self.assertTrue(any("hash crosses" in error for error in result["errors"]))

    def test_within_split_duplicate_is_warning(self):
        result = self.audit([
            {"sample_id": "a", "split": "train", "path": "a", "sha256": "a" * 64},
            {"sample_id": "b", "split": "train", "path": "b", "sha256": "a" * 64},
        ])
        self.assertTrue(any("duplicate content" in warning for warning in result["warnings"]))

    def test_empty_manifest_and_missing_required_group_fail(self):
        self.audit([], code=1)
        self.audit([{"sample_id": "a", "split": "train", "path": "a"}], "--require-groups", code=1)

    def test_file_and_label_existence(self):
        (self.base / "a").write_bytes(b"sample")
        result = self.audit([{"sample_id": "a", "split": "test", "path": "a", "label_path": "missing"}], "--check-files", code=1)
        self.assertTrue(any("label file not found" in error for error in result["errors"]))

    def test_malformed_csv_fails_cleanly(self):
        path = self.base / "manifest.csv"
        for content in (
            "sample_id,split,path\na,train\n",
            "sample_id,split,path\na,train,a,extra\n",
            "sample_id,split,path,path\na,train,a,b\n",
            'sample_id,split,path\na,train,"unterminated\n',
        ):
            with self.subTest(content=content):
                path.write_text(content)
                output = self.run_script("audit_manifest.py", path, code=1)
                self.assertTrue(json.loads(output)["errors"])

    def test_comparison_marks_incomparable_runs(self):
        for name, protocol in (("a", "v1"), ("b", "v2")):
            (self.root / "experiments" / f"{name}.md").write_text(
                f"## ID\n{name}\n## Evaluation Data ID\nvalidation-v1\n## Protocol ID\n{protocol}\n## Actual Outcome\n0.8\n"
            )
        output = self.run_script("compare_experiments.py", "--root", self.root)
        self.assertIn("do not rank", output)


if __name__ == "__main__":
    unittest.main()

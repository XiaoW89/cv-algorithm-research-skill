#!/usr/bin/env python3
"""Validate the YAML state block in a research workspace."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - handled in main
    yaml = None

STAGES = {
    "INTAKE", "PROBLEM_DEFINITION", "FEASIBILITY", "BEST_PRACTICE",
    "DATASET_RESEARCH", "DATA_ENGINEERING", "MODEL_SELECTION",
    "MODEL_DEVELOPMENT", "BASELINE", "TRAINING", "EVALUATION",
    "FAILURE_ANALYSIS", "HYPOTHESIS", "EXPERIMENT", "DELIVERY",
    "COMPLETED", "STOPPED", "PAUSED",
}
GATE_STATUSES = {"PENDING", "PASS", "BLOCKED", "NOT_APPLICABLE"}
PROJECT_STATUSES = {"ACTIVE", "BLOCKED", "PAUSED", "STOPPED", "COMPLETED"}
REQUIRED_TOP_LEVEL = {"project", "research_stage", "gates", "acceptance", "next_action", "reproduction"}
REQUIRED_GATES = {"requirements", "feasibility", "data", "baseline", "evaluation", "delivery"}
STOP_OUTCOMES = {"BEST_AVAILABLE", "BUDGET_EXHAUSTED", "INFEASIBLE", "EVIDENCE_INSUFFICIENT"}
STAGE_GATES = {
    "MODEL_DEVELOPMENT": {"requirements", "feasibility"},
    "BASELINE": {"requirements", "feasibility", "data"},
    "TRAINING": {"requirements", "feasibility", "data"},
    "EVALUATION": {"requirements", "data"},
    "EXPERIMENT": {"requirements", "feasibility", "data", "baseline"},
}


def load_state(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    blocks = re.findall(r"```yaml\s*\n(.*?)\n```", text, flags=re.DOTALL | re.IGNORECASE)
    if len(blocks) != 1:
        raise ValueError(f"expected exactly one YAML code block in {path}")
    if yaml is None:
        raise RuntimeError("PyYAML is required; install scripts/requirements.txt")

    class UniqueLoader(yaml.SafeLoader):
        pass

    def unique_mapping(loader, node, deep=False):
        result = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=deep)
            if not isinstance(key, str):
                raise ValueError("state mapping keys must be strings")
            if key in result:
                raise ValueError(f"duplicate YAML key: {key}")
            result[key] = loader.construct_object(value_node, deep=deep)
        return result

    UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)
    try:
        value = yaml.load(blocks[0], Loader=UniqueLoader)
    except yaml.YAMLError as exc:
        raise ValueError(f"invalid YAML: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError("YAML state must be a mapping")
    return value


def nonempty(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def resolve_evidence(root: Path, item: str) -> bool:
    if not isinstance(item, str) or not item.strip():
        return False
    path = Path(item)
    path = root / path if not path.is_absolute() else path
    try:
        return path.is_file() and path.stat().st_size > 0
    except OSError:
        return False


def validate(root: Path, strict: bool) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    required_files = [root / "README.md", root / "STATE.md", root / "problem" / "definition.md"]
    for path in required_files:
        if not path.exists():
            errors.append(f"missing required file: {path}")
    if errors:
        return errors, warnings

    try:
        state = load_state(root / "STATE.md")
    except (OSError, ValueError, RuntimeError) as exc:
        return [str(exc)], warnings

    def mapping(key):
        value = state.get(key)
        if not isinstance(value, dict):
            errors.append(f"{key} must be a mapping")
            return {}
        return value

    def choice(value, allowed, label):
        if not isinstance(value, str) or value not in allowed:
            errors.append(f"invalid {label}: {value!r}")

    stage = state.get("research_stage")
    choice(stage, STAGES, "research_stage")
    project = mapping("project")
    legacy = "schema_version" not in state and "gates" not in state
    if legacy:
        choice(project.get("status"), PROJECT_STATUSES | STAGES, "legacy project.status")
        for key in ("next_action", "best_checkpoint"):
            if key not in state:
                errors.append(f"legacy state missing key: {key}")
        warnings.append("Legacy state parsed; add schema_version/gates/evidence from the template before strict validation. No files changed.")
        if strict:
            errors.append("strict validation requires state schema_version 1")
        return errors, warnings

    if type(state.get("schema_version")) is not int or state["schema_version"] != 1:
        errors.append("schema_version must be integer 1")
    errors.extend(f"missing top-level state key: {key}" for key in sorted(REQUIRED_TOP_LEVEL - set(state)))
    choice(project.get("status"), PROJECT_STATUSES, "project.status")
    gates = mapping("gates")
    for name in sorted(REQUIRED_GATES - set(gates)):
        errors.append(f"missing gate: {name}")
    for name, status in gates.items():
        if name not in REQUIRED_GATES:
            errors.append(f"unknown gate: {name}")
        choice(status, GATE_STATUSES, f"gate status {name}")
    if not nonempty(state.get("next_action")):
        errors.append("next_action must be non-empty")
    reproduction = mapping("reproduction")
    acceptance = mapping("acceptance")
    accepted_statuses = {"DRAFT", "APPROVED", "ACCEPTED", "FAILED", "INSUFFICIENT_EVIDENCE"}
    choice(acceptance.get("status"), accepted_statuses, "acceptance.status")
    evidence = mapping("gate_evidence")
    gate_notes = mapping("gate_notes")
    budget = mapping("budget")
    for key in ("blockers", "open_questions"):
        if not isinstance(state.get(key), list):
            errors.append(f"{key} must be a list")
    for key in ("best_checkpoint",):
        if key not in state or (state[key] is not None and not nonempty(state[key])):
            errors.append(f"{key} must be null or a nonempty string")
    for name, status in gates.items():
        paths = evidence.get(name, [])
        if not isinstance(paths, list) or any(not nonempty(item) for item in paths):
            errors.append(f"gate_evidence.{name} must be a list of nonempty paths")
            paths = []
        if status == "PASS":
            if not isinstance(paths, list) or not paths:
                errors.append(f"gate {name} is PASS but has no gate_evidence")
            elif strict:
                for item in paths:
                    if not resolve_evidence(root, item):
                        errors.append(f"gate {name} evidence does not exist: {item!r}")
        if status == "NOT_APPLICABLE" and not nonempty(gate_notes.get(name)):
            errors.append(f"gate {name} is NOT_APPLICABLE without gate_notes")

    completed = project.get("status") == "COMPLETED"
    if completed:
        if acceptance.get("status") != "ACCEPTED":
            errors.append("COMPLETED requires acceptance.status ACCEPTED")
        if project.get("outcome") != "ACCEPTED":
            errors.append("COMPLETED requires project.outcome ACCEPTED")
    elif project.get("status") == "STOPPED":
        choice(project.get("outcome"), STOP_OUTCOMES, "stopped project.outcome")
        if not nonempty(budget.get("stop_reason")):
            errors.append("STOPPED requires budget.stop_reason")
    elif project.get("outcome") is not None:
        errors.append("active/paused/blocked project must not have a terminal outcome")
    if stage == "COMPLETED" and not completed:
        errors.append("research_stage COMPLETED requires project.status COMPLETED")
    if project.get("status") == "BLOCKED" and not state.get("blockers"):
        errors.append("BLOCKED requires at least one blocker")

    if strict:
        required = REQUIRED_GATES if completed else STAGE_GATES.get(stage, set()) if isinstance(stage, str) else set()
        if project.get("status") not in ("ACTIVE", "COMPLETED"):
            required = set()
        for name in sorted(required):
            if gates.get(name) != "PASS":
                errors.append(f"stage {stage} requires gate {name} PASS")
        if required and not nonempty(acceptance.get("contract_id")):
            errors.append("an execution stage requires acceptance.contract_id")
        if stage in ("BASELINE", "TRAINING", "EXPERIMENT") and required and not nonempty(budget.get("scope")):
            errors.append("training/experiment execution requires budget.scope")
        if completed:
            if not resolve_evidence(root, acceptance.get("evidence_path")):
                errors.append("COMPLETED requires an existing acceptance.evidence_path")
            artifacts = mapping("artifacts")
            if not resolve_evidence(root, artifacts.get("delivery")):
                errors.append("COMPLETED requires an existing artifacts.delivery path")
            if not nonempty(state.get("best_checkpoint")):
                errors.append("COMPLETED model project requires best_checkpoint")
            elif "://" not in state["best_checkpoint"] and not resolve_evidence(root, state["best_checkpoint"]):
                errors.append("best_checkpoint local file is missing or empty")
            elif "://" in state["best_checkpoint"]:
                warnings.append("Remote checkpoint existence/hash must be verified in delivery evidence.")
            for key in ("command", "config", "dataset", "code_revision", "environment"):
                if not nonempty(reproduction.get(key)):
                    errors.append(f"COMPLETED requires reproduction.{key}")

    if isinstance(stage, str) and stage in {"TRAINING", "EVALUATION", "DELIVERY", "COMPLETED"} and gates.get("data") != "PASS":
        warnings.append(f"stage {stage} has data gate {gates.get('data')!r}")
    if not nonempty(state.get("best_checkpoint")) and stage in ("DELIVERY", "COMPLETED"):
        warnings.append(f"stage {stage} has no best_checkpoint")
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("research"))
    parser.add_argument("--strict", action="store_true", help="verify evidence paths and terminal claims")
    args = parser.parse_args()
    errors, warnings = validate(args.root, args.strict)
    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        print("Research state is invalid:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("Research state is structurally valid." if not args.strict else "Research state passed strict validation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

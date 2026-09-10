"""Reconstruct the archived curated verifier experiment. Primary: ADRL-EVL-006.

Run with adrl-core on PYTHONPATH and its Python environment. This prepares local files;
it never executes the verifier, calls a model, or adopts a candidate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shlex
from pathlib import Path

from adrl.learning.improvement import AssessmentSuite, VerifierProposal, suite_digest
from adrl.ledger.session_verification import SnapshotLimits, snapshot_digest


def relative(name: str) -> Path:
    path = Path(name)
    if path.is_absolute() or ".." in path.parts or str(path) != name or name == ".":
        raise ValueError("Invalid archived relative path")
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, default=Path(__file__).with_name("adrl-improvement-inputs-2026-09-07.json"))
    parser.add_argument("--out", type=Path, required=True, help="New directory to create")
    parser.add_argument("--python", type=Path, required=True, help="Absolute adrl-core venv Python path")
    args = parser.parse_args()
    if not args.python.is_absolute() or not args.python.is_file():
        parser.error("Provide an existing absolute Python path")
    bundle = json.loads(args.bundle.read_text())
    assert bundle["schema_version"] == "verifier-experiment-input-bundle-v1"
    suite = bundle["suite"]
    proposal = bundle["proposal"]
    assert suite_digest(AssessmentSuite.model_validate(suite)) == proposal["suite_sha256"]
    for name in [*bundle["base_files"], *bundle["verifier_artifact_contents"]]:
        relative(name)
    for case in bundle["cases"]:
        relative(case["case_id"])
        for name in [*case["overrides"], *case["removed"]]:
            relative(name)
    for arm in ("baseline", "candidate"):
        for name, artifact in proposal[arm]["artifacts"].items():
            assert hashlib.sha256(bundle["verifier_artifact_contents"][name].encode()).hexdigest() == artifact["sha256"]
    out = args.out.absolute()
    out.mkdir(parents=True, exist_ok=False)
    snapshots = {item["case_id"]: item for item in suite["cases"]}
    for case in bundle["cases"]:
        workspace = out / "cases" / relative(case["case_id"])
        files = bundle["base_files"] | case["overrides"]
        for name in case["removed"]:
            del files[name]
        for name, content in files.items():
            target = workspace / relative(name)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content)
            target.chmod(0o644)
        expected = snapshots[case["case_id"]]
        assert snapshot_digest(workspace, SnapshotLimits.model_validate(suite["limits"])) == expected["snapshot_sha256"]
        expected["workspace"] = str(workspace)
    for name, content in bundle["verifier_artifact_contents"].items():
        target = out / "checks" / relative(name)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)
    for arm in ("baseline", "candidate"):
        for name, artifact in proposal[arm]["artifacts"].items():
            artifact["path"] = str(out / "checks" / relative(name))
        for check in proposal[arm]["checks"]:
            check["argv"][0] = str(args.python)
    assessment = AssessmentSuite.model_validate(suite)
    proposal["suite_sha256"] = suite_digest(assessment)
    specification = VerifierProposal.model_validate(proposal)
    specification.admit(assessment)
    (out / "suite.json").write_text(assessment.model_dump_json(indent=2) + "\n")
    (out / "proposal.json").write_text(specification.model_dump_json(indent=2) + "\n")
    print("Reconstructed and verified 7 fixed code examples and pinned verifier artifacts.")
    print("Paths were relocated and the suite digest recomputed. Review before running:")
    print(shlex.join([str(args.python), "-m", "adrl.cli.main", "improve", "evaluate", "--proposal", str(out / "proposal.json"), "--suite", str(out / "suite.json"), "--state", str(out / "state")]))


if __name__ == "__main__":
    main()

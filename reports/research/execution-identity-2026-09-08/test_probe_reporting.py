"""Offline failure recording. Primary: ADRL-OPS-001, ADRL-MEM-002."""

import ast
import json
from pathlib import Path

import pytest
from run_probe import Probe


@pytest.mark.parametrize(
    "primary,cleanup", [(False, False), (True, False), (False, True), (True, True)]
)
def test_case_and_cleanup_are_separate(tmp_path, primary, cleanup):
    p = object.__new__(Probe)
    p.output = tmp_path
    p.records = []
    p.owned = {}
    p.sequence = 0

    def create():
        p.owned["exact-receipt"] = {}
        return "exact-receipt"

    def case(*args):
        if primary:
            raise ValueError("primary_failure")
        return {"assertion_completed": True}

    def remove(identity):
        assert identity == "exact-receipt"
        if cleanup:
            raise OSError("cleanup_failure")

    p.create = create
    p.case = case
    p.remove = remove
    if primary or cleanup:
        with pytest.raises(RuntimeError):
            p.observe("reporting")
    else:
        p.observe("reporting")
    record = p.records[0]
    assert bool(record["primary_error"]) == primary
    assert bool(record["cleanup_errors"]) == cleanup
    assert bool(record.get("completed_assertions")) == (not primary)
    assert record["status"] == ("failed" if primary or cleanup else "accepted")
    checkpoints = [
        json.loads(x.read_text()) for x in sorted(tmp_path.glob("checkpoint-*.json"))
    ]
    assert checkpoints[-1]["event"] == "case_final"
    if not primary:
        assert checkpoints[-2]["event"] == "case_assertions_completed"


@pytest.mark.parametrize("receipt", [False, True])
def test_create_failure_is_retained_and_only_receipted_resources_cleaned(
    tmp_path, receipt
):
    p = object.__new__(Probe)
    p.output = tmp_path
    p.records = []
    p.owned = {}
    p.sequence = 0
    cleaned = []

    def create():
        if receipt:
            p.owned["exact-receipt"] = {}
        raise ValueError("binding_failed" if receipt else "create_uncertain")

    p.create = create
    p.remove = cleaned.append
    with pytest.raises(RuntimeError):
        p.observe("create_failure")
    assert cleaned == (["exact-receipt"] if receipt else [])
    assert p.records[0]["primary_error"]["type"] == "ValueError"
    assert p.records[0]["status"] == "failed"


def test_embedded_python_syntax():
    path = Path(__file__).with_name("run_probe.py")
    tree = ast.parse(path.read_text())
    children = [
        n.value.value
        for n in ast.walk(tree)
        if isinstance(n, ast.Assign)
        and any(isinstance(t, ast.Name) and t.id == "child" for t in n.targets)
    ]
    assert len(children) == 1
    compile(children[0], "fixture-client", "exec")

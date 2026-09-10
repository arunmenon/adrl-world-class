"""Offline recorded-pair controls. Primary: ADRL-OPS-001, ADRL-SAF-007."""

import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest
from execution_identity import compare, digest, profile

EVIDENCE = (
    Path(__file__).resolve().parents[1]
    / "adrl-w3-2b2d2-launch-contract-2026-09-08.json"
)


@pytest.fixture
def values():
    evidence = json.loads(EVIDENCE.read_text())
    pair = evidence["identity_comparison"]
    raw = []
    for which in ("before", "after"):
        data = Path(pair[which + "_path"]).read_bytes()
        assert hashlib.sha256(data).hexdigest() == pair[which + "_sha256"]
        raw.append(json.loads(data))
    p = profile(
        evidence["research_runs"][1]["engine"],
        evidence["research_runs"][1]["engine_version"],
        evidence["engine_capabilities"],
    )
    return raw[0], raw[1], p


@pytest.mark.parametrize("phase", ["created", "running"])
def test_recorded_pair(values, phase):
    before, after, p = values
    saved = deepcopy(values)
    result = compare(
        before, before if phase == "created" else after, p, p, digest(before)
    )
    assert len(result["projection_digest"]) == 64
    assert values == saved


CONTROLS = [
    ("Id", "f" * 64),
    ("Created", "2026-09-09T00:00:00Z"),
    ("Image", "sha256:" + "f" * 64),
    ("Name", "/unknown"),
    ("Path", "/other"),
    ("Args", ["other"]),
    ("Platform", "windows"),
    ("Mounts", [{"Source": "/host", "Destination": "/work"}]),
    ("Config.Cmd", ["/probe", "other"]),
    ("Config.Image", "sha256:" + "f" * 64),
    ("Config.User", "0:0"),
    ("Config.Env", ["PATH=/", "TOKEN=synthetic"]),
    ("Config.Entrypoint", ["/other"]),
    ("Config.NetworkDisabled", False),
    ("Config.WorkingDir", "/"),
    ("Config.Tty", True),
    ("Config.Labels", {"unexpected": "value"}),
    ("Config.Volumes", {"/host": {}}),
    ("Config.Healthcheck", {"Test": ["CMD", "/other"]}),
    ("Config.ExposedPorts", {"80/tcp": {}}),
    ("HostConfig.OomKillDisable", True),
    ("HostConfig.OomKillDisable", 0),
    ("HostConfig.OomKillDisable", "false"),
    ("HostConfig.PortBindings", None),
    ("HostConfig.PortBindings", {"80/tcp": [{"HostPort": "80"}]}),
    ("HostConfig.Binds", ["/host:/work"]),
    ("HostConfig.Mounts", [{"Type": "bind"}]),
    ("HostConfig.CapAdd", ["SYS_ADMIN"]),
    ("HostConfig.CapDrop", []),
    ("HostConfig.Privileged", True),
    ("HostConfig.Privileged", 0),
    ("HostConfig.SecurityOpt", ["seccomp=unconfined"]),
    ("HostConfig.Memory", 0),
    ("HostConfig.MemorySwap", 0),
    ("HostConfig.NanoCpus", 0),
    ("HostConfig.PidsLimit", 0),
    ("HostConfig.NetworkMode", "host"),
    ("HostConfig.PidMode", "host"),
    ("HostConfig.IpcMode", "host"),
    ("HostConfig.CgroupnsMode", "host"),
    ("HostConfig.Runtime", "other"),
    ("HostConfig.RestartPolicy", {"Name": "always"}),
    ("HostConfig.LogConfig", {"Type": "json-file"}),
    ("HostConfig.AutoRemove", True),
    ("HostConfig.ReadonlyRootfs", True),
    ("HostConfig.Devices", [{"PathOnHost": "/dev/x"}]),
    ("HostConfig.Unknown", None),
    ("Config.Unknown", None),
]


def alter(value, field, replacement):
    keys = field.split(".")
    for key in keys[:-1]:
        value = value[key]
    value[keys[-1]] = replacement


@pytest.mark.parametrize("field,replacement", CONTROLS)
def test_control_drift_refused(values, field, replacement):
    before, after, p = values
    alter(after, field, replacement)
    with pytest.raises(ValueError):
        compare(before, after, p, p, digest(before))


@pytest.mark.parametrize(
    "field",
    [
        "Id",
        "Created",
        "Config",
        "HostConfig",
        "Mounts",
        "Image",
        "Path",
        "Args",
        "Platform",
        "Name",
        "HostConfig.OomKillDisable",
    ],
)
def test_missing_field_refused(values, field):
    before, after, p = values
    keys = field.split(".")
    target = after if len(keys) == 1 else after[keys[0]]
    del target[keys[-1]]
    with pytest.raises(ValueError):
        compare(before, after, p, p, digest(before))


@pytest.mark.parametrize(
    "field,replacement",
    [
        ("schema", "unknown"),
        ("seccomp_sha256", "f" * 64),
        ("engine.id", "different-id"),
        ("engine.endpoint", "/different.sock"),
        ("engine.api", "1.48"),
        ("version.Version", "27.3.2"),
        ("version.KernelVersion", "other"),
        ("capabilities.OomKillDisable", True),
        ("capabilities.OomKillDisable", 0),
        ("capabilities.CgroupVersion", "1"),
        ("capabilities.MemoryLimit", False),
        ("capabilities.SwapLimit", False),
        ("capabilities.PidsLimit", False),
        ("capabilities.CpuCfsQuota", False),
        ("capabilities.CpuCfsPeriod", False),
        ("capabilities.SecurityOptions", []),
        ("capabilities.MemoryLimit", 1),
    ],
)
def test_profile_drift_refused(values, field, replacement):
    before, after, p = values
    q = deepcopy(p)
    alter(q, field, replacement)
    with pytest.raises(ValueError):
        compare(before, after, p, q, digest(before))


@pytest.mark.parametrize(
    "field", ["schema", "engine", "version", "capabilities", "seccomp_sha256"]
)
def test_missing_profile_refused(values, field):
    before, after, p = values
    q = deepcopy(p)
    del q[field]
    with pytest.raises(ValueError):
        compare(before, after, p, q, digest(before))


@pytest.mark.parametrize(
    "key",
    [
        "OomKillDisable",
        "MemoryLimit",
        "SwapLimit",
        "PidsLimit",
        "CpuCfsPeriod",
        "CpuCfsQuota",
    ],
)
def test_missing_capability_refused(values, key):
    before, after, p = values
    q = deepcopy(p)
    del q["capabilities"][key]
    with pytest.raises(ValueError):
        compare(before, after, p, q, digest(before))


@pytest.mark.parametrize("bad", [None, True, 0, "false"])
def test_original_oom_must_be_false(values, bad):
    before, after, p = values
    before["HostConfig"]["OomKillDisable"] = bad
    with pytest.raises(ValueError):
        compare(before, after, p, p, digest(before))


def test_original_digest_refused(values):
    before, after, p = values
    pinned = digest(before)
    before["Config"]["User"] = "0:0"
    with pytest.raises(ValueError, match="original_digest_changed"):
        compare(before, after, p, p, pinned)

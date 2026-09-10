"""Research execution comparison. Primary: ADRL-OPS-001. Secondary: ADRL-SAF-007.

No runtime ownership, launch, stop or capture authority. See frozen research contract v1.
"""

from __future__ import annotations

import hashlib
import json
import re
from typing import Any

SCHEMA = "execution-identity-research-v1"
SECCOMP = "9c1025c88ccaa517b648da571961838744ea2137f176bfe6a48b21294cae9c76"
CONFIG_KEYS = (
    "Config",
    "HostConfig",
    "Mounts",
    "Image",
    "Path",
    "Args",
    "Platform",
    "Name",
)
INFO_KEYS = (
    "ID",
    "OSType",
    "Architecture",
    "CgroupVersion",
    "CgroupDriver",
    "KernelVersion",
    "OomKillDisable",
    "MemoryLimit",
    "SwapLimit",
    "PidsLimit",
    "CpuCfsPeriod",
    "CpuCfsQuota",
    "SecurityOptions",
)
VERSION_KEYS = ("Version", "ApiVersion", "Os", "Arch", "KernelVersion")


def encoded(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(encoded(value)).hexdigest()


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise ValueError(reason)


def profile(
    engine: dict[str, Any], version: dict[str, Any], info: dict[str, Any]
) -> dict[str, Any]:
    value = {
        "schema": SCHEMA,
        "engine": engine,
        "version": {key: version[key] for key in VERSION_KEYS},
        "capabilities": {key: info[key] for key in INFO_KEYS},
        "seccomp_sha256": SECCOMP,
    }
    validate_profile(value)
    return value


def validate_profile(value: dict[str, Any]) -> None:
    require(
        set(value) == {"schema", "engine", "version", "capabilities", "seccomp_sha256"},
        "profile_shape",
    )
    require(
        value["schema"] == SCHEMA and value["seccomp_sha256"] == SECCOMP,
        "profile_version",
    )
    engine, version, info = value["engine"], value["version"], value["capabilities"]
    require(set(engine) == {"id", "endpoint", "api"}, "engine_shape")
    require(
        isinstance(engine["id"], str) and 8 <= len(engine["id"]) <= 256, "engine_id"
    )
    require(
        isinstance(engine["endpoint"], str)
        and engine["endpoint"].startswith("/")
        and engine["api"] == "1.47",
        "engine_endpoint",
    )
    require(
        version
        == {
            "Version": "27.3.1",
            "ApiVersion": "1.47",
            "Os": "linux",
            "Arch": "arm64",
            "KernelVersion": "6.10.11-linuxkit",
        },
        "engine_version",
    )
    require(set(info) == set(INFO_KEYS), "capability_shape")
    require(
        info["ID"] == engine["id"]
        and info["OSType"] == "linux"
        and info["Architecture"] == "aarch64",
        "engine_capability_identity",
    )
    require(
        info["CgroupVersion"] == "2"
        and info["CgroupDriver"] == "cgroupfs"
        and info["KernelVersion"] == version["KernelVersion"],
        "engine_platform",
    )
    require(info["OomKillDisable"] is False, "oom_capability")
    for key in ("MemoryLimit", "SwapLimit", "PidsLimit", "CpuCfsPeriod", "CpuCfsQuota"):
        require(info[key] is True, "required_capability_" + key)
    require(
        info["SecurityOptions"] == ["name=seccomp,profile=unconfined", "name=cgroupns"],
        "engine_security_profile",
    )


def projection(value: dict[str, Any], *, original: bool) -> dict[str, Any]:
    require(
        isinstance(value.get("Id"), str)
        and re.fullmatch(r"[a-f0-9]{64}", value["Id"]) is not None,
        "resource_id",
    )
    require(
        isinstance(value.get("Created"), str) and bool(value["Created"]),
        "resource_created",
    )
    for key in CONFIG_KEYS:
        require(key in value, "configuration_missing_" + key)
    require(
        isinstance(value["Config"], dict)
        and isinstance(value["HostConfig"], dict)
        and isinstance(value["Mounts"], list),
        "configuration_shape",
    )
    require(
        isinstance(value["Image"], str)
        and re.fullmatch(r"sha256:[a-f0-9]{64}", value["Image"]) is not None,
        "image_id",
    )
    require(
        all(isinstance(value[k], str) for k in ("Path", "Platform", "Name"))
        and isinstance(value["Args"], list),
        "command_shape",
    )
    require("OomKillDisable" in value["HostConfig"], "oom_field_missing")
    oom = value["HostConfig"]["OomKillDisable"]
    require(
        oom is False if original else oom is False or oom is None, "oom_field_value"
    )
    result = json.loads(
        encoded({key: value[key] for key in CONFIG_KEYS + ("Id", "Created")})
    )
    result["HostConfig"]["OomKillDisable"] = False
    return result


def compare(
    original: dict[str, Any],
    current: dict[str, Any],
    bound_profile: dict[str, Any],
    current_profile: dict[str, Any],
    original_digest: str,
) -> dict[str, str]:
    validate_profile(bound_profile)
    validate_profile(current_profile)
    require(
        encoded(bound_profile) == encoded(current_profile), "engine_profile_changed"
    )
    require(digest(original) == original_digest, "original_digest_changed")
    before, after = (
        projection(original, original=True),
        projection(current, original=False),
    )
    require(encoded(before) == encoded(after), "execution_configuration_changed")
    return {
        "schema": SCHEMA,
        "original_digest": original_digest,
        "profile_digest": digest(bound_profile),
        "projection_digest": digest(before),
    }

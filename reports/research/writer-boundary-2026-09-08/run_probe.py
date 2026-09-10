"""Bounded offline writer-boundary experiment. Primary: ADRL-SAF-007, ADRL-OPS-001.

Not imported by adrl-core. Uses only the provided local Docker engine, a self-authored
static Go probe and an explicit, pinned seccomp profile. No images are pulled.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import subprocess
import sys
import tarfile
import tempfile
import time
from pathlib import Path
from uuid import uuid4


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--docker-host", required=True)
    parser.add_argument("--docker", default="/usr/local/bin/docker")
    parser.add_argument("--go", default="/opt/homebrew/bin/go")
    args = parser.parse_args()
    assert args.docker_host.startswith("unix://"), "only an explicit local Unix socket"
    args.out.mkdir(mode=0o700, parents=True, exist_ok=False)
    source = Path(__file__).with_name("probe.go")
    run_id = str(uuid4())
    label = "adrl.writer-probe"
    docker = [args.docker, "--host", args.docker_host]
    report = {
        "version": "writer-boundary-probe-v1",
        "run_id": run_id,
        "status": "running",
        "source_sha256": digest(source),
        "driver_sha256": digest(Path(__file__)),
        "seccomp_sha256": digest(args.profile),
        "commands": [],
        "cases": [],
        "cleanup": [],
        "container_ids": [],
        "image_id": None,
    }
    assert json.loads(args.profile.read_text())["defaultAction"] == "SCMP_ACT_ERRNO"

    def save() -> None:
        (args.out / "result.json").write_text(json.dumps(report, indent=2) + "\n")

    def call(argv: list[str], *, env: dict | None = None, timeout: float = 15) -> str:
        started = time.monotonic()
        try:
            value = subprocess.run(
                argv, capture_output=True, text=True, env=env, timeout=timeout, check=False
            )
        except subprocess.TimeoutExpired:
            report["commands"].append({"argv": argv, "status": "timeout"})
            save()
            raise
        report["commands"].append(
            {
                "argv": argv,
                "exit_code": value.returncode,
                "seconds": round(time.monotonic() - started, 4),
                "stdout": value.stdout[:4096],
                "stderr": value.stderr[:4096],
            }
        )
        save()
        value.check_returncode()
        return value.stdout.strip()

    def inspect(identity: str) -> dict:
        values = json.loads(call(docker + ["inspect", identity]))
        assert len(values) == 1 and values[0]["Id"] == identity
        assert values[0]["Config"]["Labels"][label] == run_id
        return values[0]

    def extract(identity: str, name: str) -> Path:
        dest = args.out / name
        dest.mkdir(mode=0o700)
        call(docker + ["cp", identity + ":/work/.", str(dest)])
        return dest

    def ready(identity: str, client: subprocess.Popen | None = None) -> None:
        # Bounded inspection of our own two tiny marker files; no Docker exec process.
        for attempt in range(20):
            if client is not None and client.poll() is not None:
                raise AssertionError("owned Docker client exited before readiness")
            dest = extract(identity, "ready-" + identity[:12] + "-" + str(attempt))
            if (dest / "ready.json").exists():
                return
            time.sleep(0.05)
        raise AssertionError("container readiness not observed")

    def stopped(identity: str, expected: int) -> dict:
        code = int(call(docker + ["wait", identity]))
        state = inspect(identity)["State"]
        assert code == expected and not state["Running"] and not state["Restarting"]
        assert state["Pid"] == 0 and state["Status"] == "exited"
        return state

    def assert_fixture(root: Path) -> dict:
        value = json.loads((root / "context.json").read_text())
        assert value["pid"] == 1 and value["uid"] == value["gid"] == 65532
        assert value["CapEff"] == "0000000000000000" and value["NoNewPrivs"] == "1"
        assert value["Seccomp"] == "2" and not value["docker_socket_present"]
        assert not value["cgroup_migration_open_allowed"]
        child = json.loads((root / "child-ready.json").read_text())
        assert child["pid"] == child["group"] and child["pid"] != 1
        return {"context": value, "child": child}

    binary = args.out / "probe"
    clients: list[subprocess.Popen] = []
    try:
        call([args.go, "version"])
        env = os.environ | {
            "GOOS": "linux",
            "GOARCH": "arm64",
            "CGO_ENABLED": "0",
            "GO111MODULE": "off",
            "GOTOOLCHAIN": "local",
            "GOPROXY": "off",
            "GOSUMDB": "off",
            "GOFLAGS": "",
            "GOCACHE": str(args.out / "go-cache"),
        }
        call(
            [args.go, "build", "-trimpath", "-o", str(binary), str(source)],
            env=env,
            timeout=15,
        )
        report["binary_sha256"] = digest(binary)
        archive = args.out / "image.tar"
        with tarfile.open(archive, "w") as tar:
            for name, mode, uid in [("work", 0o700, 65532)]:
                member = tarfile.TarInfo(name)
                member.type = tarfile.DIRTYPE
                member.mode = mode
                member.uid = member.gid = uid
                tar.addfile(member)
            data = binary.read_bytes()
            member = tarfile.TarInfo("probe")
            member.mode = 0o555
            member.size = len(data)
            tar.addfile(member, io.BytesIO(data))
        image = call(
            docker
            + [
                "image",
                "import",
                "--platform",
                "linux/arm64",
                "--change",
                f"LABEL {label}={run_id}",
                str(archive),
                "adrl-writer-probe:" + run_id,
            ]
        )
        assert image.startswith("sha256:") and len(image) == 71
        report["image_id"] = image
        save()
        for mode in ["positive", "init_exit", "forced_stop", "client_death"]:
            identity = call(
                docker
                + [
                    "create",
                    "--pull=never",
                    "--name",
                    "adrl-writer-" + run_id + "-" + mode,
                    "--label",
                    f"{label}={run_id}",
                    "--label",
                    "adrl.probe-case=" + mode,
                    "--network=none",
                    "--restart=no",
                    "--user=65532:65532",
                    "--cap-drop=ALL",
                    "--security-opt=no-new-privileges=true",
                    "--security-opt=seccomp=" + str(args.profile),
                    "--pids-limit=32",
                    "--memory=96m",
                    "--memory-swap=96m",
                    "--cpus=0.5",
                    "--log-driver=none",
                    "--workdir=/work",
                    "--env=GOMAXPROCS=2",
                    image,
                    "/probe",
                    mode,
                ]
            )
            assert len(identity) == 64 and all(
                c in "0123456789abcdef" for c in identity
            )
            report["container_ids"].append(identity)
            save()
            info = inspect(identity)
            config = info["HostConfig"]
            assert info["Image"] == image and not info["Mounts"]
            assert config["NetworkMode"] == "none" and not config["Privileged"]
            assert config["PidMode"] == "" and config["RestartPolicy"]["Name"] == "no"
            assert config["PidsLimit"] == 32 and config["Memory"] == 96 * 1024 * 1024
            case = {"mode": mode, "container_id": identity}
            if mode == "client_death":
                client = subprocess.Popen(
                    docker + ["start", "--attach", identity],
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                clients.append(client)
                ready(identity, client)
                assert client.poll() is None
                client.kill()
                client.wait(timeout=3)
                case["running_after_client_death"] = inspect(identity)["State"][
                    "Running"
                ]
                assert case["running_after_client_death"]
                time.sleep(3)
                mid = extract(identity, mode + "-after-client-death")
                assert (mid / "late.txt").read_text() == "detached-late-write"
                call(docker + ["kill", "--signal=KILL", identity])
                case["state"] = stopped(identity, 137)
            else:
                call(docker + ["start", identity])
                if mode == "forced_stop":
                    ready(identity)
                    call(docker + ["kill", "--signal=KILL", identity])
                case["state"] = stopped(identity, 137 if mode == "forced_stop" else 0)
            dest = extract(identity, mode + "-stopped")
            case.update(assert_fixture(dest))
            expected = (
                "detached-late-write" if mode in {"positive", "client_death"} else ""
            )
            assert (dest / "late.txt").read_text() == expected
            if mode in {"init_exit", "forced_stop"}:
                time.sleep(2.7)
                after = extract(identity, mode + "-after-late-deadline")
                assert (after / "late.txt").read_text() == ""
                assert not inspect(identity)["State"]["Running"]
            case["result"] = "expected_observation"
            report["cases"].append(case)
            save()

        # Negative controls: opened descriptors survive chmod and a path rename.
        child_code = "import os,sys; f=os.open(sys.argv[1],os.O_WRONLY); sys.stdout.write('R'); sys.stdout.flush(); sys.stdin.read(1); os.write(f,b'changed'); os.close(f)"
        for mode in ["readonly_open_fd", "rename_open_fd"]:
            with tempfile.TemporaryDirectory(
                prefix="adrl-writer-negative-"
            ) as temporary:
                root = Path(temporary)
                original = root / "original"
                original.write_text("initial")
                child = subprocess.Popen(
                    [sys.executable, "-c", child_code, str(original)],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                )
                clients.append(child)
                assert child.stdout.read(1) == b"R"
                target = original
                if mode == "readonly_open_fd":
                    original.chmod(0o400)
                else:
                    target = root / "renamed"
                    original.rename(target)
                    original.write_text("replacement")
                child.stdin.write(b"G")
                child.stdin.flush()
                child.stdin.close()
                child.wait(timeout=3)
                assert child.returncode == 0 and target.read_text() == "changed"
                report["cases"].append(
                    {"mode": mode, "result": "existing_descriptor_still_writes"}
                )
                save()
        report["status"] = "observations_passed"
    except BaseException as exc:
        report["status"] = "failed"
        report["failure"] = {"type": type(exc).__name__, "message": str(exc)}
        raise
    finally:
        for client in clients:
            if client.poll() is None:
                client.kill()
                client.wait(timeout=3)
        clean = True
        for identity in report["container_ids"]:
            try:
                info = inspect(identity)
                assert info["Image"] == report["image_id"]
                if info["State"]["Running"]:
                    call(docker + ["kill", "--signal=KILL", identity])
                call(docker + ["rm", identity])
                report["cleanup"].append({"container_id": identity, "removed": True})
            except (OSError, ValueError, AssertionError, subprocess.SubprocessError) as exc:
                clean = False
                report["cleanup"].append(
                    {"container_id": identity, "removed": False, "error": str(exc)}
                )
        if report["image_id"] and clean:
            info = inspect(report["image_id"])
            call(docker + ["image", "rm", report["image_id"]])
            report["cleanup"].append({"image_id": report["image_id"], "removed": True})
        if not clean:
            report["status"] = "cleanup_unresolved"
        save()


if __name__ == "__main__":
    main()

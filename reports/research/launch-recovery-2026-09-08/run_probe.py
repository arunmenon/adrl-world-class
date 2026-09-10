"""Bounded synthetic launch/stop observations. Primary: ADRL-OPS-001, ADRL-SAF-007.

Research only. No runtime start/recovery capability or exact-close eligibility is added.
Run with adrl-core's existing Python environment and one explicit private fixture JSON.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import socket
import socketserver
import subprocess
import sys
import tarfile
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from datetime import UTC, datetime
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from typing import Any
from urllib.parse import quote
from uuid import uuid4

import httpx

from adrl.core.container_control import (
    ContainerControl,
    ContainerRequest,
    EngineError,
    ResourcePolicy,
    canonical,
)


class Probe:
    def __init__(self, fixture: dict[str, Any], output: Path) -> None:
        self.fixture = fixture
        self.output = output
        self.output.mkdir(mode=0o700)
        self.log = Path(fixture["resource_log"])
        profile = Path(fixture["profile"]).read_bytes()
        assert hashlib.sha256(profile).hexdigest() == (
            "9c1025c88ccaa517b648da571961838744ea2137f176bfe6a48b21294cae9c76"
        )
        self.control = ContainerControl(
            Path(fixture["socket"]),
            profile,
            hashlib.sha256(profile).hexdigest(),
            ResourcePolicy(request_seconds=2),
        )
        self.engine = self.control.engine()
        version = self.control._request("GET", "/version")
        assert version["Version"] == "27.3.1" and version["ApiVersion"] == "1.47"
        self.records: list[dict[str, Any]] = []
        self.owned: dict[str, dict[str, Any]] = {}
        self.version = version

    def record(self, value: dict[str, Any]) -> None:
        value = {"at": datetime.now(UTC).isoformat()} | value
        with self.log.open("a") as out:
            out.write(json.dumps(value, sort_keys=True) + "\n")
            out.flush()
            os.fsync(out.fileno())

    def create(self) -> str:
        records = (
            [json.loads(line) for line in self.log.read_text().splitlines()]
            if self.log.exists()
            else []
        )
        assert sum(r["event"] == "create_receipt" for r in records) < 12
        assert self.control.engine() == self.engine
        operation = hashlib.sha256(uuid4().bytes).hexdigest()
        request = ContainerRequest(
            image_id=self.fixture["image_id"], argv=("/probe", "forced_stop")
        )
        name, body = self.control.prepare(request, operation)
        identity = self.control.create(name, body)
        self.owned[identity] = {"name": name, "body": body}
        self.record(
            {"event": "create_receipt", "id": identity, "name": name, "image": request.image_id}
        )
        value = self.control.inspect(identity)
        self.control.verify_created(value, name, body)
        self.owned[identity]["configuration"] = self.control.configuration(value)
        self.owned[identity]["created"] = value["Created"]
        (self.output / (identity + ".created.json")).write_text(json.dumps(value, indent=2) + "\n")
        return identity

    def inspect(self, identity: str) -> dict[str, Any]:
        assert identity in self.owned and self.control.engine() == self.engine
        value = self.control.inspect(identity)
        expected = self.owned[identity]
        assert (
            value["Image"] == self.fixture["image_id"] and value["Name"] == "/" + expected["name"]
        )
        assert value["Created"] == expected["created"]
        actual_config = self.control.configuration(value)
        if actual_config != expected["configuration"]:
            (self.output / (identity + ".changed.json")).write_text(
                json.dumps(value, indent=2) + "\n"
            )
        before = json.loads(canonical(expected["configuration"]))
        after = json.loads(canonical(actual_config))
        # Research-only candidate normalization. Both representations must mean no ports;
        # all other Config/HostConfig/identity fields retain exact comparison.
        for config in (before, after):
            assert config["HostConfig"]["PortBindings"] in (None, {})
            config["HostConfig"]["PortBindings"] = {}
        assert before == after
        return value

    def start(self, identity: str) -> None:
        self.inspect(identity)
        self.control._request("POST", f"/containers/{identity}/start")

    def kill(self, identity: str) -> int:
        self.inspect(identity)
        try:
            self.control._request("POST", f"/containers/{identity}/kill?signal=KILL")
        except EngineError as exc:
            return exc.status
        return 204

    def remove(self, identity: str) -> None:
        try:
            self.inspect(identity)
        except EngineError as exc:
            assert exc.status == 404
        else:
            self.control._request("DELETE", f"/containers/{identity}?force=true&v=false")
        try:
            self.control.inspect(identity)
        except EngineError as exc:
            assert exc.status == 404
        else:
            raise AssertionError("owned_resource_remains")
        self.record({"event": "absent", "id": identity})

    def file(self, identity: str, name: str) -> bytes | None:
        assert name in {"ready.json", "late.txt", "context.json"}
        path = quote("/work/" + name, safe="")
        transport = httpx.HTTPTransport(uds=str(self.control.socket), retries=0)
        with httpx.Client(
            transport=transport, trust_env=False, timeout=2, follow_redirects=False
        ) as client:
            with client.stream(
                "GET",
                f"http://localhost/v1.47/containers/{identity}/archive?path={path}",
                headers={"Accept-Encoding": "identity"},
            ) as response:
                if response.status_code == 404:
                    return None
                assert response.status_code == 200
                assert response.headers.get("Content-Encoding", "identity") == "identity"
                data = bytearray()
                for chunk in response.iter_raw():
                    data.extend(chunk)
                    assert len(data) <= 131072
        with tarfile.open(fileobj=io.BytesIO(data)) as archive:
            members = archive.getmembers()
            assert len(members) == 1
            member = members[0]
            assert member.name == name and member.isfile() and member.size <= 8192
            handle = archive.extractfile(member)
            assert handle is not None
            return handle.read(8193)

    def ready(self, identity: str) -> None:
        deadline = time.monotonic() + 2
        while time.monotonic() < deadline:
            if self.file(identity, "ready.json") is not None:
                return
            time.sleep(0.02)
        raise AssertionError("fixture_not_ready")

    def exited(self, identity: str, seconds: float = 2) -> dict[str, Any]:
        deadline = time.monotonic() + seconds
        while time.monotonic() < deadline:
            value = self.inspect(identity)
            if value["State"]["Status"] == "exited" and not value["State"]["Running"]:
                return value
            time.sleep(0.025)
        raise AssertionError("fixture_exit_unconfirmed")

    @contextmanager
    def delayed(self, identity: str, *, lose_reply: bool = False):
        arrived, forward = threading.Event(), threading.Event()
        control = self.control
        result: dict[str, Any] = {}
        with tempfile.TemporaryDirectory(prefix="adrl-launch-", dir="/tmp") as directory:
            endpoint = str(Path(directory) / "gate.sock")

            class Handler(BaseHTTPRequestHandler):
                def log_message(self, format: str, *args: Any) -> None:
                    pass

                def do_POST(self) -> None:
                    assert self.path == f"/v1.47/containers/{identity}/start"
                    arrived.set()
                    assert forward.wait(5)
                    try:
                        control._request("POST", f"/containers/{identity}/start")
                    except EngineError as exc:
                        result["upstream_status"] = exc.status
                    else:
                        result["upstream_status"] = 204
                    if lose_reply:
                        self.connection.shutdown(socket.SHUT_RDWR)
                        self.connection.close()
                        return
                    self.send_response(result["upstream_status"])
                    self.send_header("Content-Length", "0")
                    self.end_headers()

            server = socketserver.ThreadingUnixStreamServer(endpoint, Handler)
            server.daemon_threads = True
            thread = threading.Thread(target=server.serve_forever, kwargs={"poll_interval": 0.01})
            thread.start()

            def client() -> None:
                transport = httpx.HTTPTransport(uds=endpoint, retries=0)
                try:
                    with httpx.Client(
                        transport=transport, trust_env=False, timeout=2
                    ) as connection:
                        response = connection.post(
                            f"http://localhost/v1.47/containers/{identity}/start"
                        )
                        result["client_status"] = response.status_code
                except httpx.HTTPError:
                    result["client_status"] = "lost"

            pool = ThreadPoolExecutor(max_workers=1)
            future = pool.submit(client)
            try:
                assert arrived.wait(2)
                yield forward, future, result
            finally:
                forward.set()
                future.result(timeout=3)
                pool.shutdown(wait=True)
                server.shutdown()
                server.server_close()
                thread.join(timeout=2)

    def observe(self, case: str) -> dict[str, Any]:
        identity = self.create()
        started = time.monotonic()
        try:
            if case == "kill_before_delayed_start":
                with self.delayed(identity) as (gate, future, transport):
                    kill_status = self.kill(identity)
                    assert kill_status == 409
                    self.control.never_started(self.inspect(identity))
                    gate.set()
                    future.result(timeout=3)
                assert transport["client_status"] == 204
                self.ready(identity)
                time.sleep(2.7)
                late = self.file(identity, "late.txt")
                assert late == b"detached-late-write"
                outcome = {"kill_status": kill_status, "transport": transport, "late_write": True}
            elif case == "remove_before_delayed_start":
                with self.delayed(identity) as (gate, future, transport):
                    self.remove(identity)
                    gate.set()
                    future.result(timeout=3)
                assert transport["client_status"] == 404 and transport["upstream_status"] == 404
                outcome = {"transport": transport, "removed_before_forward": True}
            elif case == "lost_start_ack_then_discard":
                with self.delayed(identity, lose_reply=True) as (gate, future, transport):
                    gate.set()
                    future.result(timeout=3)
                assert transport == {"upstream_status": 204, "client_status": "lost"}
                self.ready(identity)
                active = self.inspect(identity)["State"]["Running"]
                assert active
                self.remove(identity)
                try:
                    self.control._request("POST", f"/containers/{identity}/start")
                except EngineError as exc:
                    assert exc.status == 404
                else:
                    raise AssertionError("removed_resource_started")
                outcome = {
                    "transport": transport,
                    "active_without_client_ack": active,
                    "discarded": True,
                }
            elif case == "known_start_stop_preserves_output":
                self.start(identity)
                self.ready(identity)
                assert self.kill(identity) == 204
                value = self.exited(identity)
                before = self.file(identity, "late.txt")
                time.sleep(2.7)
                after = self.file(identity, "late.txt")
                assert before == after == b""
                context = json.loads(self.file(identity, "context.json") or b"null")
                assert context["Seccomp"] == "2" and context["NoNewPrivs"] == "1"
                assert int(context["CapEff"], 16) == 0
                outcome = {
                    "state": value["State"],
                    "output_unchanged": True,
                    "late_write": False,
                    "context": context,
                }
            elif case == "exited_resource_can_restart":
                self.start(identity)
                self.ready(identity)
                initial = self.inspect(identity)
                assert self.kill(identity) == 204
                self.exited(identity)
                self.start(identity)
                self.ready(identity)
                again = self.inspect(identity)
                assert initial["State"]["StartedAt"] != again["State"]["StartedAt"]
                assert initial["RestartCount"] == again["RestartCount"] == 0
                time.sleep(2.7)
                assert self.file(identity, "late.txt") == b"detached-late-write"
                outcome = {
                    "first_started_at": initial["State"]["StartedAt"],
                    "second_started_at": again["State"]["StartedAt"],
                    "restart_count": again["RestartCount"],
                    "late_write_after_restart": True,
                }
            else:
                assert case == "client_death_fixture_deadline"
                child = """
import json, os, sys, httpx
v=json.loads(sys.stdin.readline())
transport=httpx.HTTPTransport(uds=v['socket'], retries=0)
with httpx.Client(transport=transport,trust_env=False,timeout=2) as client:
    response=client.post('http://localhost/v1.47/containers/'+v['id']+'/start')
    assert response.status_code == 204
    os._exit(23)
"""
                result = subprocess.run(
                    [sys.executable, "-c", child],
                    input=json.dumps({"socket": str(self.control.socket), "id": identity}),
                    capture_output=True,
                    text=True,
                    timeout=3,
                )
                assert result.returncode == 23
                self.ready(identity)
                assert self.inspect(identity)["State"]["Running"]
                value = self.exited(identity, seconds=9)
                duration = datetime.fromisoformat(
                    value["State"]["FinishedAt"].replace("Z", "+00:00")
                ) - datetime.fromisoformat(value["State"]["StartedAt"].replace("Z", "+00:00"))
                assert duration.total_seconds() <= 8
                outcome = {
                    "client_exit_code": 23,
                    "active_after_client_exit": True,
                    "fixture_elapsed_seconds": duration.total_seconds(),
                    "state": value["State"],
                }
            elapsed = time.monotonic() - started
            assert elapsed <= 15
            return {
                "case": case,
                "status": "observed",
                "resource_id": identity,
                "elapsed_seconds": elapsed,
                "observation": outcome,
            }
        finally:
            self.remove(identity)

    def run(self) -> None:
        cases = [
            "kill_before_delayed_start",
            "remove_before_delayed_start",
            "lost_start_ack_then_discard",
            "known_start_stop_preserves_output",
            "exited_resource_can_restart",
            "client_death_fixture_deadline",
        ]
        result = {
            "schema_version": "adrl-launch-recovery-observations-v1",
            "engine": self.engine,
            "engine_version": self.version,
            "started_at": datetime.now(UTC).isoformat(),
            "observations": self.records,
            "status": "running",
        }
        path = self.output / "observations.json"
        try:
            for case in cases:
                path.write_text(json.dumps(result, indent=2) + "\n")
                observation = self.observe(case)
                self.records.append(observation)
                print(case, "observed", flush=True)
            result["status"] = "completed"
        except Exception as exc:
            result["status"] = "failed"
            result["error_type"] = type(exc).__name__
            raise
        finally:
            result["finished_at"] = datetime.now(UTC).isoformat()
            result["created_ids"] = list(self.owned)
            path.write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    Probe(json.loads(args.fixture.read_text()), args.output).run()

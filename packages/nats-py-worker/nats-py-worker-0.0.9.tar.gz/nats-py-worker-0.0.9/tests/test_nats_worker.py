import contextlib
import os
import signal
import subprocess
import tempfile
from pathlib import Path
from random import randint

import pytest
import asyncio
from nats_worker import Worker


class NATSD:
    """
    Starts a local NATS server for testing.
    Originally from: https://github.com/nats-io/nats.py/blob/main/tests/utils.py
    """

    def __init__(
        self,
        port=4222,
        user="",
        password="",
        token="",
        timeout=0,
        http_port=8222,
        debug=False,
        tls=False,
        cluster_listen=None,
        routes=None,
        config_file=None,
        with_jetstream=None,
    ):
        self.port = port
        self.user = user
        self.password = password
        self.timeout = timeout
        self.http_port = http_port
        self.proc = None
        self.tls = tls
        self.token = token
        self.cluster_listen = cluster_listen
        self.routes = routes or []
        self.bin_name = "nats-server"
        self.config_file = config_file
        self.debug = debug or os.environ.get("DEBUG_NATS_TEST") == "true"
        self.with_jetstream = with_jetstream
        self.store_dir = None

        if with_jetstream:
            self.store_dir = tempfile.mkdtemp()

    def start(self):
        # Default path
        if Path(self.bin_name).is_file():
            self.bin_name = Path(self.bin_name).absolute()

        cmd = [
            self.bin_name,
            "-p",
            "%d" % self.port,
            "-m",
            "%d" % self.http_port,
            "-a",
            "127.0.0.1",
        ]
        if self.user:
            cmd.append("--user")
            cmd.append(self.user)
        if self.password:
            cmd.append("--pass")
            cmd.append(self.password)

        if self.token:
            cmd.append("--auth")
            cmd.append(self.token)

        if self.debug:
            cmd.append("-DV")

        if self.with_jetstream:
            cmd.append("-js")
            cmd.append(f"-sd={self.store_dir}")

        if self.tls:
            cmd.append("--tls")
            cmd.append("--tlscert")
            cmd.append("certs/server-cert.pem")
            cmd.append("--tlskey")
            cmd.append("certs/server-key.pem")
            cmd.append("--tlsverify")
            cmd.append("--tlscacert")
            cmd.append("certs/ca.pem")

        if self.cluster_listen is not None:
            cmd.append("--cluster_listen")
            cmd.append(self.cluster_listen)

        if len(self.routes) > 0:
            cmd.append("--routes")
            cmd.append(",".join(self.routes))
            cmd.append("--cluster_name")
            cmd.append("CLUSTER")

        if self.config_file is not None:
            cmd.append("--config")
            cmd.append(self.config_file)

        if self.debug:
            self.proc = subprocess.Popen(cmd)
        else:
            self.proc = subprocess.Popen(
                cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )

        if self.debug:
            if self.proc is None:
                print(
                    "[\031[0;33mDEBUG\033[0;0m] Failed to start server listening on port %d started."
                    % self.port
                )
            else:
                print(
                    "[\033[0;33mDEBUG\033[0;0m] Server listening on port %d started."
                    % self.port
                )
        return self.proc

    def stop(self):
        if self.debug:
            print(
                "[\033[0;33mDEBUG\033[0;0m] Server listening on %d will stop."
                % self.port
            )

        if self.debug:
            if self.proc is None:
                print(
                    "[\033[0;31mDEBUG\033[0;0m] Failed terminating server listening on port %d"
                    % self.port
                )

        if self.proc.returncode is not None:
            if self.debug:
                print(
                    "[\033[0;31mDEBUG\033[0;0m] Server listening on port {port} finished running already with exit {ret}".format(
                        port=self.port, ret=self.proc.returncode
                    )
                )
        else:
            os.kill(self.proc.pid, signal.SIGKILL)
            self.proc.wait()
            if self.debug:
                print(
                    "[\033[0;33mDEBUG\033[0;0m] Server listening on %d was stopped."
                    % self.port
                )


@contextlib.contextmanager
def test_servers():
    random_port = randint(49152, 64535)
    nats_server = NATSD(
        port=random_port, http_port=random_port + 1000, with_jetstream=True
    )
    try:
        nats_server.start()
        yield f"nats://127.0.0.1:{random_port}"
    finally:
        nats_server.stop()


def test_create_worker():
    Worker(name="test")


def test_create_worker_no_name():
    with pytest.raises(TypeError):
        Worker()


@pytest.mark.asyncio
async def test_worker_start_stop():
    with test_servers() as servers:
        worker = Worker(name="test", servers=servers)

        result = None

        async def fast_task(*, connection):
            nonlocal result
            result = "success"
            await worker.stop()

        worker.schedule(fast_task)

        await asyncio.wait_for(worker.start(), 10)

        assert result == "success"


@pytest.mark.asyncio
async def test_worker_with_worker_publish():
    with test_servers() as servers:
        async with Worker(name="test", servers=servers) as worker:
            await worker.connection.jetstream().add_stream(
                name="TEST", subjects=["test"]
            )
            await worker.publish_msg(b"test", subject="test")


@pytest.mark.asyncio
async def test_worker_failure():
    with test_servers() as servers:
        worker = Worker(name="test", servers=servers)

        message = "Workers should stop on unhandled exceptions"

        async def failing_task(*, connection):
            raise RuntimeError(message)

        worker.schedule(failing_task)

        try:
            await asyncio.wait_for(worker.start(), timeout=10)
            assert False, "Worker should have failed"
        except RuntimeError as ex:
            assert ex.args[0] == message, message

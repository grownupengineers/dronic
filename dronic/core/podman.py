# may fail if not installed, so import it first
import podman

import io
import pathlib
import random
import secrets
import tarfile
import time

from multiprocessing.managers import BaseManager

from dronic.plugin import AgentPlugin
from dronic._config import CONFIG


class PodmanManager(BaseManager):
    pass


PodmanManager.register("do_stage")
PodmanManager.register("do_shutdown")


class PodmanAgent(AgentPlugin):

    description = "Podman agent manager"
    version = "0.0.1"
    author = "dronic"

    def __init__(self):
        self._cli = podman.from_env()

    def initialize(self):
        pass

    def finalize(self):
        pass

    def can_provide(self, podman_str=None, *args, **kwds):
        return podman_str == "podman"

    def provision(self, _podman_str, image, *args, **kwds):
        pm = self._cli

        # 1. pull image

        try:
            image = pm.images.get(image)
        except podman.errors.ImageNotFound:
            image = pm.images.pull(image)

        # 2. create container

        # can be hardcoded, will be random on the host
        a_port = str(50004)
        a_password = secrets.token_urlsafe(16)
        a_workspace = "/" + secrets.token_urlsafe(8)
        command = [
            "dronic-cli",
            # TODO dump config somewhere and add it here
            "--agent",
            "--agent-password",
            a_password,
            "--agent-port",
            a_port,
            "--workspace",
            a_workspace,
            CONFIG["jobfile"],
            *CONFIG["params"],
        ]

        port_key = f"{a_port}/tcp"

        container = pm.containers.create(
            image,
            command,
            ports={port_key: None},  # use random host port
            working_dir=a_workspace,
            # TODO params from args/kwds
        )

        host_port = container.ports[port_key][0]

        # 3. copy workspace
        tar_fileobj = io.BytesIO()
        with tarfile.open(fileobj=tar_fileobj, mode="w|") as tar:
            # TODO read from config (or special file)
            ignore_globs = (
                "__pycache__",
                "*.pyc",
            )

            def filter(ti: tarfile.TarInfo) -> "tarfile.TarInfo|None":
                ti.name = ti.name.lstrip("/")
                if ti.name == "":
                    return ti
                path = pathlib.Path(ti.name)
                par = path
                while par.name != "":
                    for glob in ignore_globs:
                        if par.match(glob):
                            return None
                    par = par.parent
                return ti  # original

            tar.add(
                CONFIG["workspace"],
                arcname=a_workspace.lstrip('/'),
                filter=filter
            )

        container.put_archive("/", tar_fileobj.getvalue())
        # 4. launch container + dronic --agent
        container.start()

        # 5. create manager + connect to container agent
        manager = PodmanManager(
            address=(host_port["HostIp"], int(host_port["HostPort"])),
            authkey=a_password.encode(),
        )
        manager.connect()
        manager._container = container
        return manager

    def shutdown(self, manager):
        container = manager._container
        # 1. stop container (remove it?)
        manager.do_shutdown()
        container.stop()
        # 2. copy workspace (changes) back?
        # probably need a way to have "artifacts"

        container.remove()


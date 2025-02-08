#
# A manager for multiprocessing
#

import os
import multiprocessing
from multiprocessing import Event
from multiprocessing.managers import BaseManager

from . import StageClass

class AgentManager(BaseManager):
    pass


def do_stage(stage_id: int):
    stage = StageClass.get_stage(stage_id)
    if stage is None:
        raise Exception("Stage not found")
    stage.run()


shutdown_event = Event()


def do_shutdown():
    # TODO figure out a way to notify the manager/server to stop
    # no stop server or anything
    # exit(0)
    shutdown_event.set()


def init_manager(args) -> "tuple[AgentManager,Event]":

    AgentManager.register("do_stage", do_stage)
    AgentManager.register("do_shutdown", do_shutdown)

    return (
        AgentManager(
            address=("0.0.0.0", args.agent_port),
            authkey=str.encode(args.agent_password),
        ),
        shutdown_event,
    )


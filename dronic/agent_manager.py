#
# A manager for multiprocessing
#

import os
import multiprocessing
from multiprocessing.managers import BaseManager


class AgentManager(multiprocessing.managers.BaseManager):
    pass


def do_stage(stage_id: int):
    stage = StageClass.get_stage(stage_id)
    if stage is None:
        raise Exception("Stage not found")
    stage.run()


def do_shutdown():
    # no stop server or anything
    exit(0)


def init_manager(args) -> AgentManager:

    AgentManager.register("do_stage", do_stage)
    AgentManager.register("do_shutdown", do_shutdown)

    return AgentManager(
        address=("0.0.0.0", args.agent_port), authkey=str.encode(args.agent_password)
    )

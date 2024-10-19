#
# Parallel context manager
#

#
# inserts a wrapper stage that executes internals stages in parallel
#
# this is done by temporarily hijacking the StageClass's CONTAINER
#

import multiprocessing as mp
import types

from . import StageClass


class Parallel(object):
    """
    Stages defined inside a Pipeline context will get executed in parallel
    """

    def __init__(self):
        self._stages = []
        self._save = None

    def __enter__(self):
        self._save = StageClass.hijack(self._stages)

    def __exit__(self, _type, value, traceback):
        StageClass.restore(self._save)
        parallel_stage = StageClass("Parallel")(self._runner)

    def _runner(self):
        processes = []
        for stage in self._stages:
            # it's not really read vs write, it's more
            # "we're using one for read and another for write"
            pipe_r, pipe_w = mp.Pipe()
            proc = mp.Process(
                target=types.MethodType(self._stage_wrapper, stage), args=(pipe_w,)
            )
            processes.append((proc, pipe_r))
            proc.start()

        last_exc = None
        result_merged = True
        for p, r in processes:
            result, exc = r.recv()
            p.join()
            if exc is not None:
                last_exc = exc
            if result is not None:
                # this is not good, as 0 usually means success but evaluates
                # as False
                result_merged = result_merged and bool(result)
        if last_exc is not None:
            raise last_exc
        return result_merged

    def _stage_wrapper(self, stage, conn) -> tuple[object, Exception]:
        try:
            result = stage.run()
            conn.send((result, None))
        except Exception as e:
            conn.send((None, e))

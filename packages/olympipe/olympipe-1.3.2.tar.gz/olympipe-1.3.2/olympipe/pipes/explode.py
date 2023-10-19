from multiprocessing.managers import DictProxy
from typing import Callable, Iterable, List, TypeVar

from olympipe.pipes.task import TaskPipe
from olympipe.shuttable_queue import ShuttableQueue

R = TypeVar("R")
S = TypeVar("S")


class ExplodePipe(TaskPipe[R, S]):
    def __init__(
        self,
        father_process_dag: "DictProxy[str, List[str]]",
        source: "ShuttableQueue[R]",
        task: Callable[[R], Iterable[S]],
        target: "ShuttableQueue[S]",
    ):
        super().__init__(father_process_dag, source, task, target)  # type: ignore

    def _send_to_next(self, processed: Iterable[S]):  # type: ignore
        for p in processed:
            super()._send_to_next(p)

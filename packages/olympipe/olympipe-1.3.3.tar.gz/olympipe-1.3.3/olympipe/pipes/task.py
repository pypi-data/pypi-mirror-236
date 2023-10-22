from multiprocessing.managers import DictProxy
from typing import Callable, List, TypeVar

from olympipe.shuttable_queue import ShuttableQueue

from .generic import GenericPipe

R = TypeVar("R")
S = TypeVar("S")


class TaskPipe(GenericPipe[R, S]):
    def __init__(
        self,
        father_process_dag: "DictProxy[str, List[str]]",
        source: "ShuttableQueue[R]",
        task: Callable[[R], S],
        target: "ShuttableQueue[S]",
    ):
        self._task = task
        super().__init__(father_process_dag, source, target)

    @property
    def shortname(self) -> str:
        return self._task.__name__

    def _perform_task(self, data: R) -> S:
        return self._task(data)

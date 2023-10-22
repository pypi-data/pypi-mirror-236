from multiprocessing.managers import DictProxy
from typing import Callable, List, TypeVar

from olympipe.shuttable_queue import ShuttableQueue

from .generic import GenericPipe

R = TypeVar("R")


class FilterPipe(GenericPipe[R, R]):
    def __init__(
        self,
        father_process_dag: "DictProxy[str, List[str]]",
        source: "ShuttableQueue[R]",
        task: Callable[[R], bool],
        target: "ShuttableQueue[R]",
    ):
        self._task = task
        super().__init__(father_process_dag, source, target)

    @property
    def shortname(self) -> str:
        return f"filter:{self._task.__name__}"

    def _perform_task(self, data: R) -> R:
        if self._task(data):
            super()._send_to_next(data)
        return data

    def _send_to_next(self, processed: R):
        pass

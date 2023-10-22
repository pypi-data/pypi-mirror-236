from multiprocessing.managers import DictProxy
from typing import List, TypeVar

from olympipe.shuttable_queue import ShuttableQueue

from .generic import GenericPipe

R = TypeVar("R")


class DebugPipe(GenericPipe[R, R]):
    def __init__(
        self,
        father_process_dag: "DictProxy[str, List[str]]",
        source: "ShuttableQueue[R]",
        target: "ShuttableQueue[R]",
    ):
        super().__init__(father_process_dag, source, target)

    @property
    def shortname(self) -> str:
        return "_"

    def _perform_task(self, data: R) -> R:
        print(self.__repr__().replace("_", str(self.pid)), data)
        return data

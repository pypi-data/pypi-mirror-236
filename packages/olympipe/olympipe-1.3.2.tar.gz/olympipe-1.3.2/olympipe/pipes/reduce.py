from multiprocessing.managers import DictProxy
import queue
from typing import Callable, List, TypeVar

from olympipe.shuttable_queue import ShuttableQueue

from .generic import GenericPipe

R = TypeVar("R")
T = TypeVar("T")


class ReducePipe(GenericPipe[R, T]):
    def __init__(
        self,
        father_process_dag: "DictProxy[str, List[str]]",
        source: "ShuttableQueue[R]",
        target: "ShuttableQueue[T]",
        accumulator: T,
        reducer: Callable[[R, T], T],
    ):
        self._accumulator = accumulator
        self._reduce_function = reducer
        super().__init__(father_process_dag, source, target)

    def _perform_task(self, data: R) -> None:  # type: ignore
        self._accumulator = self._reduce_function(data, self._accumulator)

    def _kill(self):
        self._send_to_next(self._accumulator)
        super()._kill()

    def run(self):
        while True:
            try:
                data = self._source_queue.get(timeout=self._timeout)
                self._perform_task(data)
            except queue.Empty:
                pass
            except Exception as e:
                print(f"Error_{e.__class__.__name__}_{e.args}")
                self._kill()
                break
            if self.can_quit():
                self._kill()
                break

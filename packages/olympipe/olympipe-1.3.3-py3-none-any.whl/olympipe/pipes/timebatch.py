import time
from multiprocessing.managers import DictProxy
from queue import Empty
from typing import List, Optional, TypeVar

from olympipe.shuttable_queue import ShuttableQueue

from .generic import GenericPipe

R = TypeVar("R")
S = TypeVar("S")
T = TypeVar("T")


class TimeBatchPipe(GenericPipe[R, List[R]]):
    def __init__(
        self,
        father_process_dag: "DictProxy[str, List[str]]",
        source: "ShuttableQueue[R]",
        target: "ShuttableQueue[List[R]]",
        interval: float,
    ):
        self._interval: float = interval
        self._timeout: float = interval
        self._datas: List[R] = []
        self._last_time = time.time()
        super().__init__(father_process_dag, source, target)

    @property
    def shortname(self) -> str:
        return f"TBatch:{self._interval}s"

    def _perform_task(self, data: R) -> Optional[List[R]]:  # type: ignore
        elapsed = time.time() - self._last_time
        self._timeout = self._last_time + self._interval - time.time()
        if elapsed >= self._interval:
            self.increment_timeout()
            packet = self._datas[:]
            self._datas.clear()
            self._datas.append(data)
            return packet
        self._datas.append(data)
        return None

    def increment_timeout(self):
        self._last_time += self._interval
        self._timeout += self._interval

    def _send_to_next(self, processed: List[R]):
        super()._send_to_next(processed)

    def run(self):
        while True:
            try:
                data = self.get_next()
                processed = self._perform_task(data)
                if processed is not None:
                    self._send_to_next(processed)
            except Empty:
                pass
            except TimeoutError:
                self._send_to_next(self._datas)
                self._datas = []
            except Exception as e:
                print(self.__repr__(), "Error", e)
            if self.can_quit():
                self._send_to_next(self._datas)
                self._kill()
                break

from multiprocessing.managers import DictProxy
import queue
from typing import List, Optional, TypeVar

from olympipe.shuttable_queue import ShuttableQueue
from olympipe.pipes.generic import GenericPipe

R = TypeVar("R")


class BatchPipe(GenericPipe[R, List[R]]):
    def __init__(
        self,
        father_process_dag: "DictProxy[str, List[str]]",
        source: "ShuttableQueue[R]",
        target: "ShuttableQueue[List[R]]",
        batch_size: int,
        keep_incomplete_batch: bool,
    ):
        self._batch_size = batch_size
        self._datas: List[R] = []
        self._keep_incomplete_batch = keep_incomplete_batch
        super().__init__(father_process_dag, source, target)

    def _perform_task(self, data: R) -> Optional[List[R]]:  # type: ignore
        self._datas.append(data)
        if len(self._datas) >= self._batch_size:
            packet, self._datas = (
                self._datas[: self._batch_size],
                self._datas[self._batch_size :],
            )
            return packet

    def _send_to_next(self, processed: Optional[List[R]]) -> None:
        if processed is None:
            return
        super()._send_to_next(processed)

    def run(self):
        while True:
            try:
                data = self._source_queue.get(timeout=self._timeout)
                processed = self._perform_task(data)
                self._send_to_next(processed)
            except queue.Empty:
                pass
            except Exception as e:
                print(f"Error_{e.__class__.__name__}_{e.args}")
                self._kill()
                return
            if self.can_quit():
                if self._keep_incomplete_batch:
                    self._send_to_next(self._datas)
                self._kill()
                return

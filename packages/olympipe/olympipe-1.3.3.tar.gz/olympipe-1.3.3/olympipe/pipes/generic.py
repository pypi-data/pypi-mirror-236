import copy
from multiprocessing import Process
from multiprocessing.managers import DictProxy
from queue import Empty, Full
from typing import Dict, Generic, List, Optional, Tuple, TypeVar, cast

import psutil
import setproctitle

from olympipe.shuttable_queue import ShuttableQueue

R = TypeVar("R")
S = TypeVar("S")


class GenericPipe(Process, Generic[R, S]):
    DEBUG = False

    def __init__(
        self,
        father_process_dag: "DictProxy[str, List[str]]",
        source: "ShuttableQueue[R]",
        target: "ShuttableQueue[S]",
    ):
        self._father_process_dag = father_process_dag
        self._timeout: Optional[float] = 0.1
        self._source_queue = source
        self._target_queue = target
        setproctitle.setproctitle(self.__repr__())
        super().__init__(daemon=True)
        self.start()

    def can_quit(self) -> bool:
        # check no fathers && input queue empty
        pid = str(self.pid)
        has_living_father = False
        with self._father_process_dag._mutex:
            frozen_dag: Dict[str, List[str]] = copy.deepcopy(
                self._father_process_dag._getvalue()
            )

            if pid in frozen_dag:
                for f_queue in frozen_dag[pid]:
                    if f_queue in frozen_dag:
                        for p_children in frozen_dag[f_queue]:
                            try:
                                has_living_father = (
                                    psutil.pid_exists(int(p_children))
                                    or has_living_father
                                )
                            except Exception as e:
                                print("Could not eval can_quit", pid, f_queue, e)

            is_queue_empty = self._source_queue.empty()
        return (not has_living_father) and is_queue_empty

    def get_ends(self) -> "Tuple[ShuttableQueue[R], Process, ShuttableQueue[S]]":
        return (self._source_queue, self, self._target_queue)

    def unregister_from_dag(self):
        pid = str(self.pid)
        frozen_dag: Dict[str, List[str]] = copy.deepcopy(
            self._father_process_dag._getvalue()
        )
        keys_to_delete: List[str] = []
        for key, pids in frozen_dag.items():
            if pid in pids:
                filtered_pids = [p for p in pids if p != pid]
                if len(filtered_pids) > 0:
                    self._father_process_dag[key] = filtered_pids

                else:
                    keys_to_delete.append(key)
                    self._source_queue.close()
        for key in keys_to_delete:
            _ = self._father_process_dag.pop(key)

        if pid in frozen_dag:
            _ = self._father_process_dag.pop(pid)

    @property
    def shortname(self) -> str:
        return "Generic"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}[{self.shortname}]"

    def _kill(self):
        with self._father_process_dag._mutex:
            self.unregister_from_dag()

    def _perform_task(self, data: R) -> S:
        return cast(S, data)

    def _send_to_next(self, processed: S):
        while True:
            try:
                self._target_queue.put(processed, timeout=self._timeout)
                break
            except (Full, TimeoutError):
                pass
            except Exception as e:
                print("next", e)
                raise e

    def get_next(self) -> R:
        return cast(R, self._source_queue.get(timeout=self._timeout))

    def run(self):
        while True:
            try:
                data = self.get_next()
                processed = self._perform_task(data)
                self._send_to_next(processed)
            except (TimeoutError, Empty, Full):
                pass
            except Exception as e:
                print(self.__repr__(), "Error", e)
                pass
            if self.can_quit():
                self._kill()
                break

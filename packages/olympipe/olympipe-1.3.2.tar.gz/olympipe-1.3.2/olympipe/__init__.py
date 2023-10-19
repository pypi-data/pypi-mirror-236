__version__ = "1.3.2"

from multiprocessing.managers import DictProxy
import os
import time
from multiprocessing import Manager, TimeoutError
from queue import Empty, Full
from threading import Timer
from typing import Any, Callable, Dict, Generic, Iterable, List, Optional, TypeVar


from olympipe.pipes.batch import BatchPipe
from olympipe.pipes.explode import ExplodePipe
from olympipe.pipes.filter import FilterPipe
from olympipe.pipes.instance import ClassInstancePipe
from olympipe.pipes.reduce import ReducePipe
from olympipe.pipes.task import TaskPipe
from olympipe.pipes.timebatch import TimeBatchPipe
from olympipe.shuttable_queue import ShuttableQueue

R = TypeVar("R")
S = TypeVar("S")
T = TypeVar("T")


class Pipeline(Generic[T]):
    def __init__(
        self,
        datas: Optional[Iterable[T]] = None,
        source: Optional["ShuttableQueue[Any]"] = None,
        output_queue: Optional["ShuttableQueue[T]"] = None,
        father_process_dag: Optional["DictProxy[str, List[str]]"] = None,
    ):
        if father_process_dag is None:
            self._manager = Manager()
            self._father_process_dag: "DictProxy[str, List[str]]" = self._manager.dict()
            self._father_process_dag._mutex = (
                self._manager.Lock()
            )  # Important! base lock not working
        else:
            self._father_process_dag = father_process_dag

        self._source_queue = source
        self._output_queue: "ShuttableQueue[T]" = (
            Pipeline.get_new_queue() if output_queue is None else output_queue
        )
        self._datas = datas
        self._last_debug_hash = ""
        self._started = True
        if father_process_dag is None:
            self._started = False
            Timer(0, self.start).start()
        while not self._started:
            time.sleep(0.1)

    @staticmethod
    def get_new_queue() -> "ShuttableQueue[Any]":
        queue: "ShuttableQueue[Any]" = ShuttableQueue()
        return queue

    def start(self):
        self._father_process_dag[self._output_queue.pid] = [str(os.getpid())]
        self._started = True
        if self._datas is not None:
            for data in self._datas:
                while True:
                    try:
                        self._output_queue.put(data, timeout=0.1)
                        break
                    except Exception:
                        pass
        while not self._output_queue.empty():
            time.sleep(0.1)
        while self._source_queue is not None and not self._source_queue.empty():
            time.sleep(0.1)

        with self._father_process_dag._mutex:
            _ = self._father_process_dag.pop(self._output_queue.pid)

    def register_father_son(self, father: str, son: str):
        with self._father_process_dag._mutex:
            dag: Dict[str, List[str]] = self._father_process_dag._getvalue()
            if father not in dag:
                self._father_process_dag[father] = [son]
            else:
                self._father_process_dag[father] = [
                    *dag[father],
                    son,
                ]

    def task(self, task: Callable[[T], S], count: int = 1) -> "Pipeline[S]":
        assert count >= 1

        output_task_queue: "ShuttableQueue[S]" = Pipeline.get_new_queue()

        for _ in range(count):
            p = TaskPipe(
                self._father_process_dag,
                self._output_queue,
                task,
                output_task_queue,
            )

            self.register_father_son(str(p.pid), self._output_queue.pid)
            self.register_father_son(output_task_queue.pid, str(p.pid))

        return Pipeline(
            source=self._output_queue,
            output_queue=output_task_queue,
            father_process_dag=self._father_process_dag,
        )

    def class_task(
        self,
        class_constructor: Any,
        class_method: Callable[[Any, T], S],
        class_args: List[Any] = [],
        close_method: Optional[Callable[[Any], Any]] = None,
        class_kwargs: Dict[str, Any] = {},
        count: int = 1,
    ) -> "Pipeline[S]":
        assert count >= 1
        output_task_queue: "ShuttableQueue[S]" = Pipeline.get_new_queue()

        for _ in range(count):
            p = ClassInstancePipe(
                self._father_process_dag,
                self._output_queue,
                class_constructor,
                class_method,
                output_task_queue,
                close_method,
                class_args,
                class_kwargs,
            )

            self.register_father_son(str(p.pid), self._output_queue.pid)
            self.register_father_son(output_task_queue.pid, str(p.pid))

        return Pipeline(
            source=self._output_queue,
            output_queue=output_task_queue,
            father_process_dag=self._father_process_dag,
        )

    def explode(self, explode_function: Callable[[T], Iterable[S]]) -> "Pipeline[S]":
        output_task_queue: "ShuttableQueue[S]" = Pipeline.get_new_queue()

        p = ExplodePipe(
            self._father_process_dag,
            self._output_queue,
            explode_function,
            output_task_queue,
        )

        self.register_father_son(str(p.pid), self._output_queue.pid)
        self.register_father_son(output_task_queue.pid, str(p.pid))

        return Pipeline(
            source=self._output_queue,
            output_queue=output_task_queue,
            father_process_dag=self._father_process_dag,
        )

    def batch(
        self, batch_size: int = 2, keep_incomplete_batch: bool = True
    ) -> "Pipeline[List[T]]":
        output_task_queue: "ShuttableQueue[List[T]]" = Pipeline.get_new_queue()
        p = BatchPipe(
            self._father_process_dag,
            self._output_queue,
            output_task_queue,
            batch_size,
            keep_incomplete_batch,
        )

        self.register_father_son(str(p.pid), self._output_queue.pid)
        self.register_father_son(output_task_queue.pid, str(p.pid))

        return Pipeline(
            source=self._output_queue,
            output_queue=output_task_queue,
            father_process_dag=self._father_process_dag,
        )

    def temporal_batch(self, time_interval: float) -> "Pipeline[List[T]]":
        output_task_queue: "ShuttableQueue[List[T]]" = Pipeline.get_new_queue()
        p = TimeBatchPipe(
            self._father_process_dag,
            self._output_queue,
            output_task_queue,
            time_interval,
        )

        self.register_father_son(str(p.pid), self._output_queue.pid)
        self.register_father_son(output_task_queue.pid, str(p.pid))

        return Pipeline(
            source=self._output_queue,
            output_queue=output_task_queue,
            father_process_dag=self._father_process_dag,
        )

    def filter(self, filter_function: Callable[[T], bool]) -> "Pipeline[T]":
        output_task_queue: "ShuttableQueue[T]" = Pipeline.get_new_queue()

        p = FilterPipe(
            self._father_process_dag,
            self._output_queue,
            filter_function,
            output_task_queue,
        )

        self.register_father_son(str(p.pid), self._output_queue.pid)
        self.register_father_son(output_task_queue.pid, str(p.pid))

        return Pipeline(
            source=self._output_queue,
            output_queue=output_task_queue,
            father_process_dag=self._father_process_dag,
        )

    @staticmethod
    def print_return(data: S) -> S:
        print(f"debug_pipe {data}")
        return data

    def debug(self) -> "Pipeline[T]":
        return self.task(Pipeline.print_return)

    def reduce(self, accumulator: R, reducer: Callable[[T, R], R]) -> "Pipeline[R]":
        output_task_queue: "ShuttableQueue[R]" = Pipeline.get_new_queue()

        p = ReducePipe(
            self._father_process_dag,
            self._output_queue,
            output_task_queue,
            accumulator,
            reducer,
        )

        self.register_father_son(str(p.pid), self._output_queue.pid)
        self.register_father_son(output_task_queue.pid, str(p.pid))

        return Pipeline(
            source=self._output_queue,
            output_queue=output_task_queue,
            father_process_dag=self._father_process_dag,
        )

    def wait_and_reduce(
        self,
        accumulator: R,
        reducer: Callable[[T, R], R],
    ) -> "R":
        output_pipeline = self.reduce(accumulator, reducer)
        [[res]] = Pipeline._wait_for_all_results([output_pipeline])
        return res

    @staticmethod
    def are_pipelines_running(pipes: List["Pipeline[Any]"]) -> bool:
        mutexs: List[Any] = []
        for p in pipes:
            m = p._father_process_dag._mutex
            if m not in mutexs:
                mutexs.append(m)
        for m in mutexs:
            m.acquire()

        remaining_dag = any([len(p._father_process_dag) > 0 for p in pipes])

        full_pipe = any([not p._output_queue.empty() for p in pipes])
        for m in mutexs:
            m.release()

        return remaining_dag or full_pipe

    @staticmethod
    def _wait_for_all_completions(
        pipes: List["Pipeline[Any]"], debug_graph: Optional[str] = None
    ) -> None:
        while Pipeline.are_pipelines_running(pipes):
            if debug_graph is not None:
                pipes[0].print_graph(debug_graph)
            for i, p in enumerate(pipes):
                try:
                    _: Any = p._output_queue.get(timeout=0.1)
                except TimeoutError:
                    pass
                except Full:
                    pass
                except Empty:
                    pass
                except Exception as e:
                    _ = pipes.pop(i)
                    print("Error waiting:", e)

    @staticmethod
    def _wait_for_all_results(
        pipes: List["Pipeline[Any]"], debug_graph: Optional[str] = None
    ) -> List[List[Any]]:
        final_queues: List[Optional[ShuttableQueue[Any]]] = [
            p._output_queue for p in pipes
        ]
        outputs: List[List[Any]] = [[] for _ in pipes]
        while Pipeline.are_pipelines_running(pipes):
            if debug_graph is not None:
                pipes[0].print_graph(debug_graph)
            for i, final_queue in enumerate(final_queues):
                if final_queue is None:
                    continue
                try:
                    packet: Any = final_queue.get(timeout=0.1)
                    outputs[i].append(packet)
                except TimeoutError:
                    pass
                except Full:
                    pass
                except Empty:
                    pass
                except Exception as e:
                    print("Error waiting:", e)

        return outputs

    def wait_for_completion(
        self, other_pipes: List["Pipeline[Any]"] = [], debug_graph: Optional[str] = None
    ) -> None:
        """_summary_

        Args:
            other_pipes (List[&quot;Pipeline[Any]&quot;], optional): _description_. Defaults to [].

        Returns:
            _type_: _description_
        """
        return Pipeline._wait_for_all_completions([self, *other_pipes], debug_graph)

    def wait_for_results(
        self, other_pipes: List["Pipeline[Any]"] = [], debug_graph: Optional[str] = None
    ) -> List[List[T]]:
        """_summary_

        Args:
            other_pipes (List[&quot;Pipeline[Any]&quot;], optional): _description_. Defaults to [].

        Returns:
            List[List[R]]: _description_
        """
        return Pipeline._wait_for_all_results([self, *other_pipes], debug_graph)

    def wait_for_result(self, debug_graph: Optional[str] = None) -> List[T]:
        """
        Args:

        Returns:
            Iterable[R]: _description_
        """
        res: List[List[T]] = Pipeline._wait_for_all_results([self], debug_graph)

        return res[0]

    def print_graph(self, debug_graph: str):
        try:
            import hashlib

            from graphviz import Digraph  # type: ignore

            dot = Digraph("G", filename=debug_graph, format="png")

            with self._father_process_dag._mutex:
                dag: Dict[str, List[str]] = self._father_process_dag._getvalue()
                for node, parents in dag.items():
                    dot.node(node, node)

                    for parent in parents:
                        if parent not in dag:
                            dot.node(parent, parent)

                        if parent:
                            dot.edge(parent, node)

                # Create a new SHA-256 hash object
                sha256 = hashlib.sha256()
                sha256.update(dot.source.encode())
                computed_hash = sha256.hexdigest()
                if computed_hash != self._last_debug_hash:
                    self._last_debug_hash = computed_hash
                    _ = dot.render(quiet=True, cleanup=True)

        except Exception as e:
            print(e)

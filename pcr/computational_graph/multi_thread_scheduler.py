from pcr.computational_graph.scheduler import Scheduler
from pcr.logger.log_util import logger

from concurrent.futures.thread import ThreadPoolExecutor
import multiprocessing


class MultiThreadScheduler(Scheduler):
    def __init__(self, computational_graph):
        super().__init__(computational_graph)

    def schedule(self):
        pool = ThreadPoolExecutor(max_workers=multiprocessing.cpu_count())
        task_futures = []
        for task in self._computational_graph.tasks():
            task_futures.append((task, pool.submit(task.execute)))
            logger.debug("schedule task in multi thread scheduler", task=str(task))
        for (task, task_future) in task_futures:
            task_future.result()
            logger.debug("task completed in multi thread scheduler", task=str(task))
        pool.shutdown()
        logger.debug("shutdown thread pool in multi thread scheduler")

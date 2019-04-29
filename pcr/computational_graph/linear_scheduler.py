from pcr.computational_graph.scheduler import Scheduler
from pcr.logger.log_util import logger


class LinearScheduler(Scheduler):
    def __init__(self, computational_graph):
        super().__init__(computational_graph)

    def schedule(self):
        """execute all tasks in topological order"""
        for task in self._computational_graph.tasks():
            task.execute()
            logger.debug("schedule task in linear scheduler", task=str(task))
        logger.debug("all tasks completed in linear scheduler")

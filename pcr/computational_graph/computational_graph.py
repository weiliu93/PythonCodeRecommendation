from pcr.computational_graph.graph_edge import GraphEdge
from pcr.logger.log_util import logger

from collections import deque


class ComputationalGraph(object):
    def __init__(self):
        self._task_set = set()

    def add_task(self, task):
        self._task_set.add(task)
        logger.debug("add new task", task=str(task))
        return self

    def add_edge(self, from_task, to_task):
        """add a new edge between from task and to task"""
        self._task_set.add(from_task)
        self._task_set.add(to_task)
        edge = GraphEdge(from_task.graph_node, to_task.graph_node)
        from_task.graph_node.out_edges.add(edge)
        to_task.graph_node.in_edges.add(edge)
        logger.debug("add new edge", from_task=str(from_task), to_task=str(to_task))
        return self

    def reset(self):
        for task in self._task_set:
            # cleanup in_edge and out_edge set directly
            graph_node = task.graph_node
            graph_node.in_edges.clear()
            graph_node.out_edges.clear()

    def tasks(self):
        """all tasks in topological order"""
        node_to_task_dict = {task.graph_node: task for task in self._task_set}
        queue, in_degree_dict = deque(), {}
        for task in self._task_set:
            if not task.graph_node.in_edges:
                queue.append(task.graph_node)
            in_degree_dict[task.graph_node] = len(task.graph_node.in_edges)
        while queue:
            current_node = queue.popleft()
            yield node_to_task_dict[current_node]
            for edge in current_node.out_edges:
                in_degree_dict[edge.to_node] -= 1
                if in_degree_dict[edge.to_node] == 0:
                    queue.append(edge.to_node)

    def validate(self):
        """validate if it is a legal graph"""
        queue, in_degree_dict = deque(), {}
        for task in self._task_set:
            if not task.graph_node.in_edges:
                queue.append(task.graph_node)
            in_degree_dict[task.graph_node] = len(task.graph_node.in_edges)
        cnt = 0
        while queue:
            current_node = queue.popleft()
            cnt += 1
            for edge in current_node.out_edges:
                in_degree_dict[edge.to_node] -= 1
                if in_degree_dict[edge.to_node] == 0:
                    queue.append(edge.to_node)
        if cnt != len(self._task_set):
            raise Exception("cycle detected in computing graph")

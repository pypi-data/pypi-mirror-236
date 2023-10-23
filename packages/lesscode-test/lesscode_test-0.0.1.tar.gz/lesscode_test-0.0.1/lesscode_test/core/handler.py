from typing import List

import gevent
from gevent import monkey
from gevent.pool import Pool

from lesscode_test.core.task_handle import Task
from lesscode_test.core.task_info import TaskInfo

monkey.patch_all()


class Handler:
    def __init__(self, task_list: List[TaskInfo], num: int = None):
        pool_num = num if num else len(task_list)
        self.task_list = task_list
        self.p = Pool(pool_num)
        self.results = []

    def run(self):
        if self.task_list:
            tasks = [self.p.spawn(Task(task_info=task).handle) for task in self.task_list if
                     isinstance(task, TaskInfo)]
            if tasks:
                gevent.joinall(tasks)
                self.results = [_.value for _ in tasks]
        return self.results

import copy
import importlib
import traceback

from lesscode_options.options import define, options

from lesscode_test.core.result import Result
from lesscode_test.core.task_info import TaskInfo

define(name="task_func_lib_path", type_=str, default=f'task.task_func',
       help_="任务函数库路径", callback=str)


class TaskResult:
    def __init__(self, task_info: TaskInfo, result: Result):
        self.task_info = task_info
        self.result = result

    def __dict__(self):
        task_result = copy.deepcopy(self.task_info.__dict__())
        task_result.update(self.result.__dict__())
        return task_result


class Task:
    def __init__(self, task_info: TaskInfo):
        self.task_info = task_info
        self.retry_times = 0

    def handle(self):
        result = None
        pre_func = None
        func = None
        back_func = None
        try:
            task_func = importlib.import_module(options.task_func_lib_path)
        except ImportError:
            task_func = importlib.import_module(self.task_info.task_func_lib_path)
        if self.task_info.pre_func_name:
            pre_func = getattr(task_func, self.task_info.pre_func_name) \
                if hasattr(task_func, self.task_info.pre_func_name) else None
        if self.task_info.func_name:
            func = getattr(task_func, self.task_info.func_name) \
                if hasattr(task_func, self.task_info.func_name) else None
        if self.task_info.back_func_name:
            back_func = getattr(task_func, self.task_info.back_func_name) \
                if hasattr(task_func, self.task_info.back_func_name) else None
        if pre_func:
            self.task_info = pre_func(self.task_info)
        if not self.task_info.is_skip:
            if func:
                if self.task_info.times:
                    for i in range(self.task_info.times):
                        self.retry_times = i
                        try:
                            result = func(task_info=self.task_info)
                            break
                        except Exception as e:
                            result = Result(status_code=500,
                                            response=None, error=traceback.format_exc(), is_success=False)
                    if result and isinstance(result, Result):
                        result.retry_times = self.retry_times
            else:
                result = Result(status_code=500,
                                response=None, error=f"{self.task_info.func_name}函数不存在", is_success=False)
        else:
            result = Result(status_code=200, response=None, error=None, is_success=True)
        if result and isinstance(result, Result):
            result.is_skip = self.task_info.is_skip
        if back_func:
            result = back_func(result)
        if isinstance(result, Result):
            return TaskResult(task_info=self.task_info, result=result)
        else:
            result = Result(status_code=500,
                            response=None, error="格式不正确", is_success=False)
            result.is_skip = self.task_info.is_skip
            return TaskResult(task_info=self.task_info, result=result)

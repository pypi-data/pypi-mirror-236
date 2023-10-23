import uuid
from typing import Any


class TaskInfo:
    def __init__(self, task_name, times: int = 3, project_name: str = "",
                 url: str = '', resource_type: str = "", resource_name: str = "", is_auth: bool = False,
                 params: Any = None, headers: Any = None, func_name: str = None, pre_func_name: str = None,
                 back_func_name: str = None, method: str = "GET", is_skip: bool = False,
                 task_func_lib_path: str = None):
        self.task_id = uuid.uuid4().hex
        self.task_name = task_name
        self.times = times
        self.project_name = project_name
        self.url = url
        self.resource_type = resource_type
        self.resource_name = resource_name
        self.is_auth = is_auth
        self.params = params
        self.headers = headers
        self.pre_func_name = pre_func_name
        self.func_name = func_name
        self.back_func_name = back_func_name
        self.method = method
        self.is_skip = is_skip
        self.task_func_lib_path = task_func_lib_path

    def __dict__(self):
        return {"project_name": self.project_name, "url": self.url, "resource_type": self.resource_type,
                "resource_name": self.resource_name, "task_id": self.task_id, "task_name": self.task_name,
                "is_auth": self.is_auth, "params": self.params, "headers": self.headers,
                "method": self.method.upper() if self.method else "GET", "is_skip": self.is_skip}

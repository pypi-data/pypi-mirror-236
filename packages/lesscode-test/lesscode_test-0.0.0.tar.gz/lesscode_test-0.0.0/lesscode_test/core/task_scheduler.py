import uuid
from typing import List

from apscheduler.events import JobExecutionEvent
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.base import STATE_RUNNING

from core.handler import Handler
from core.parse_data import parse_yaml, parse_json
from core.task_handle import TaskInfo, TaskResult


def run_task(task_list: List[TaskInfo], scheduler: BackgroundScheduler):
    # 运行任务，调用顺序2
    def run():
        results = Handler(task_list).run()
        return results

    if scheduler.state == STATE_RUNNING:
        task_id = uuid.uuid1().hex
        scheduler.add_job(func=run, id=task_id, name="run")
    else:
        raise Exception("运行任务失败，原因是BackgroundScheduler没有启动")


def set_task_list(yaml_path: str = None, json_path: str = None, data: dict = None):
    # 设置任务，调用顺序1
    task_list = []
    config = None
    if yaml_path:
        config = parse_yaml(yaml_path)
    elif json_path:
        config = parse_json(json_path)
    elif data:
        config = data
    if isinstance(config, dict):
        projects = config.get("projects")
        if isinstance(projects, list):
            for project in config.get("projects"):
                if isinstance(project, dict):
                    resources = project.get("resources")
                    base_url = project.get("base_url")
                    project_name = project.get("name")
                    if isinstance(resources, list):
                        for resource in resources:
                            if isinstance(resource, dict):
                                task_name = resource.get("task_name")
                                url = base_url + resource.get("path")
                                is_auth = bool(resource.get("is_auth", False)) or False
                                params = resource.get("params")
                                headers = resource.get("headers")
                                method = resource.get("method") if resource.get("method") else "GET"
                                task_list.append(TaskInfo(task_name=task_name,
                                                          times=int(resource.get("times", 1)) if resource.get(
                                                              "times") else 1,
                                                          project_name=project_name,
                                                          url=url, resource_type=resource.get("type"),
                                                          resource_name=resource.get("name"),
                                                          is_auth=is_auth, params=params, headers=headers,
                                                          func_name=resource.get("func_name"),
                                                          pre_func_name=resource.get("pre_func_name"),
                                                          back_func_name=resource.get("back_func_name"),
                                                          method=method,
                                                          is_skip=resource.get("is_skip", False) if resource.get(
                                                              "is_skip") else False,
                                                          task_func_lib_path=resource.get("task_func_lib_path")))
    return task_list


def set_listener(receive_result_func, scheduler: BackgroundScheduler):
    # 设置监听，调用顺序1
    def listener(event):
        if isinstance(event, JobExecutionEvent):
            retval = event.retval
            if retval and isinstance(retval, list):
                results = [_ for _ in retval if isinstance(_, TaskResult)]
                if receive_result_func:
                    receive_result_func(results)

    if scheduler.state == STATE_RUNNING:
        scheduler.add_listener(listener)
    else:
        raise Exception("设置监听失败，原因是BackgroundScheduler没有启动")


def run_scheduler(yaml_path: str = None, json_path: str = None, data: dict = None, receive_result_func=None):
    scheduler = BackgroundScheduler()
    scheduler.start()
    task_list = set_task_list(yaml_path=yaml_path, json_path=json_path, data=data)
    run_task(task_list=task_list, scheduler=scheduler)
    set_listener(receive_result_func=receive_result_func, scheduler=scheduler)

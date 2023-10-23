from core.handler import Handler
from core.job import JobInfo
from core.task_scheduler import set_task_list


def patrol_task(yaml_path: str = None, json_path: str = None, data: dict = None):
    task_list = set_task_list(yaml_path=yaml_path, json_path=json_path, data=data)
    results = Handler(task_list).run()
    return results


def get_cronjob_list(config_path):
    job_list = [
        JobInfo(func=patrol_task, name="巡检任务", hour=14, minute=22, func_kwargs={"config_path": config_path})]
    return job_list

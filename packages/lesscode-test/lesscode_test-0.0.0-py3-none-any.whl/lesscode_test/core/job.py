import logging
import uuid
from datetime import datetime, tzinfo
from typing import Union

from apscheduler.events import JobExecutionEvent


class JobInfo:
    def __init__(self, func, name: str = None, year: Union[int, str] = None, month: Union[int, str] = None,
                 day: Union[int, str] = None,
                 week: Union[int, str] = None, day_of_week: Union[int, str] = None,
                 hour: Union[int, str] = None, minute: Union[int, str] = None, second: Union[int, str] = None,
                 start_date: Union[datetime, str] = None, end_date: Union[datetime, str] = None,
                 timezone: Union[tzinfo, str] = None, func_args: Union[list, tuple] = None, func_kwargs: dict = None,
                 *args, **kwargs):
        uid = uuid.uuid4().hex
        self.id = uid
        self.name = name or uid
        self.func = func
        self.year = year
        self.month = month
        self.day = day
        self.week = week
        self.day_of_week = day_of_week
        self.hour = hour
        self.minute = minute
        self.second = second
        self.start_date = start_date
        self.end_date = end_date
        self.timezone = timezone
        self.func_args = func_args
        self.func_kwargs = func_kwargs
        self.args = args
        self.kwargs = kwargs


def job_listener(event):
    if isinstance(event, JobExecutionEvent):
        """
        JobExecutionEvent
            job_id 任务的标识ID
            jobstore 包含相关任务的任务存储的别名
            scheduled_run_time 计划运行任务的时间
            retval 成功执行的任务的返回值
            exception 任务运行引起的异常
            traceback 任务出错的位置
        """
        logging.info(f"job_id={event.job_id}")
        logging.info(f"jobstore={event.jobstore}")
        logging.info(f"scheduled_run_time={event.scheduled_run_time}")
        logging.info(f"retval={event.retval}")
        logging.info(f"exception={event.exception}")

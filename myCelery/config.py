import logging

import djcelery
from celery.schedules import crontab

djcelery.setup_loader()
#  任务队列的连接地址
BROKER_URL = 'redis://47.98.224.226:6379/15'

# 结果队列的地址
CELERY_RESULT_BACKEND = 'redis://47.98.224.226:6379/14'

# 结果序列化方案
CELERY_RESULT_SERIALIZER = 'json'

CELERYD_MAX_TASKS_PER_CHILD = 100  # 每个worker最大执行数，长时间执行造成内存泄露/
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
CELERYD_HIJACK_ROOT_LOGGER = False  # 拦截根日志配置
from celery._state import get_current_task

# class Formatter(logging.Formatter):
#     """Formatter for tasks, adding the task name and id."""
#
#     def format(self, record):
#         task = get_current_task()
#         if task and task.request:
#             record.__dict__.update(task_id='%s ' % task.request.id,
#                                    task_name='%s ' % task.name)
#         else:
#             record.__dict__.setdefault('task_name', '')
#             record.__dict__.setdefault('task_id', '')
#         return logging.Formatter.format(self, record)


# root_logger = logging.getLogger()  # 返回logging.root
# root_logger.setLevel(logging.DEBUG)
#
# # 将日志输出到文件
# fh = logging.FileHandler('celery_worker.log')  # 这里注意不要使用TimedRotatingFileHandler，celery的每个进程都会切分，导致日志丢失
# formatter = Formatter(
#     '[%(task_name)s%(task_id)s%(process)s %(thread)s %(asctime)s %(pathname)s:%(lineno)s] %(levelname)s: %(message)s',
#     datefmt='%Y-%m-%d %H:%M:%S')
# fh.setFormatter(formatter)
# fh.setLevel(logging.DEBUG)
# root_logger.addHandler(fh)
from logging.handlers import TimedRotatingFileHandler


# class Configlg(object):
#     # 设置日志
#     log_fmt = '%(asctime)s\tFile \"%(filename)s\",line %(lineno)s\t%(levelname)s: %(message)s'
#
#     # log_file_handler = TimedRotatingFileHandler(filename="log", when="MIDNIGHT", interval=1, backupCount=30)
#     log_file_handler = TimedRotatingFileHandler(filename="log", when="M", interval=1, backupCount=7)
#     formatter = logging.Formatter(log_fmt)
#     log_file_handler.setFormatter(formatter)
#
#     logging.basicConfig(format=log_fmt)
#     LOGGER = logging.getLogger()
#     LOGGER.setLevel(logging.INFO)
#
#     LOGGER.addHandler(log_file_handler)

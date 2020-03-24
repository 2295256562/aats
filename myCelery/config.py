import djcelery
from celery.schedules import crontab

djcelery.setup_loader()
#  任务队列的连接地址
BROKER_URL = 'redis://127.0.0.1:6379/15'

# 结果队列的地址
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/14'

# 结果序列化方案
CELERY_RESULT_SERIALIZER = 'json'

CELERYD_MAX_TASKS_PER_CHILD = 100 # 每个worker最大执行数，长时间执行造成内存泄露/
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"


from datetime import timedelta

# CELERYBEAT_SCHEDULE = {
#     'add-every-30-seconds': {
#         'task': 'add',
#         'schedule': timedelta(seconds=10),
#         'args': (16, 16)
#     },
# }
# CELERYBEAT_SCHEDULE = {
#     'every-minute': {
#         'task': 'proj.tasks.add',
#         'schedule': crontab(minute='*/1'),
#         'args': (1,2),
#     },
# }
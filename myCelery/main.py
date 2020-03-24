from __future__ import absolute_import
from celery import Celery
from myCelery import config

import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aats.settings")
# # 创建celery实例对象
app = Celery("aats")
#
# # 通过app加载配置
app.config_from_object("myCelery.config")
# # 加载任务
#
# # 参数必须是一个列表,里面的每一个任务都是任务的路径名称
app.autodiscover_tasks(["myCelery.run_case", 'myCelery.add'])
#

# app.conf.enable_utc = False
# app.conf.timezone = "Asia/Shanghai"
# app.conf.timezone = 'UTC'

#
# #  启动celery命令
# # celery -A main worker --loglevel=info

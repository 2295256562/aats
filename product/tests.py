import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aats.settings")
django.setup()
import time
import datetime
from django.db.models import Count

from aats.settings import BASE_DIR
from product.models import ApiCase

from django.test import TestCase
import json

# # Create your tests here.
# list = ['sfwf', [2,3,4], 35, 'fsf']
# print(list)
# c = (json.dumps(list))
# print(json.loads(c))
# from product.models import Project


# MEDIA_ROOT = os.path.join(BASE_DIR, 'avatar')
# print(MEDIA_ROOT)


queryset = ApiCase.objects.extra(select={"create_time": "DATE_FORMAT(create_time, '%%Y-%%m-%%d')"}).values(
    "create_time").annotate(count=Count("id")).order_by()
print(queryset)

count_data = ApiCase.objects.filter(create_time__year=2020, create_time__month=3) \
    .extra(select={"create_time": "DATE_FORMAT(create_time,'%%e')"}).values('create_time') \
    .annotate(send_num=Count('create_time')).values('create_time')



#当前日期格式
cur_date = datetime.datetime.now().date()
#前一天日期
yester_day = cur_date - datetime.timedelta(days=1)
#前一周日期
week = cur_date - datetime.timedelta(days=30)


#查询前一周数据,也可以用range,我用的是glt,lte大于等于
obj_list=ApiCase.objects.filter(create_time__gte=week, create_time__lte=cur_date)
print(obj_list)

c  = "2020-04-02 14:49:07,494 - INFO: 用例ID:7↵2020-04-02 14:49:07,497 - INFO: 请求方式:2↵2020-04-02 14:49:07,499 - INFO: 请求url:http://api.dlab.com/app/user/login/v2↵2020-04-02 14:49:07,500 - INFO: 请求headers:{'Content-Type': 'application/json', 'api-version': 'v1.2.0', 'request-source': 'web', 'authorization': '${data.token}'}↵2020-04-02 14:49:07,500 - INFO: 请求参数:{'mobile': '17671105406', 'password': 'yuanman99'}↵2020-04-02 14:49:07,655 - INFO: 响应结果:{'flag': True, 'msg': 'success', 'code': 0, 'data': {'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjo0ODc4NzU4LCJleHAiOjE1ODY0MTQ5NDcsImlhdCI6MTU4NTgxMDE0N30.8bWuEkH42_4OgBNw-S8WpbE0juntMf6aOejmME55qqk', 'uid': 4878758}}↵2020-04-02 14:49:07,656 - INFO: 校验方式:json_response↵2020-04-02 14:49:07,656 - INFO: 校验值[{'key': '$.code', 'value': '0', 'initiate': true}]"

s_replace = c.replace('↵', '</br>',)
print(s_replace)

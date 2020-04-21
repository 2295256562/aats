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

# # # Create your tests here.
# # list = ['sfwf', [2,3,4], 35, 'fsf']
# # print(list)
# # c = (json.dumps(list))
# # print(json.loads(c))
# # from product.models import Project
#
#
# # MEDIA_ROOT = os.path.join(BASE_DIR, 'avatar')
# # print(MEDIA_ROOT)
#
#
# queryset = ApiCase.objects.extra(select={"create_time": "DATE_FORMAT(create_time, '%%Y-%%m-%%d')"}).values(
#     "create_time").annotate(count=Count("id")).order_by()
# print(queryset)
#
# count_data = ApiCase.objects.filter(create_time__year=2020, create_time__month=3) \
#     .extra(select={"create_time": "DATE_FORMAT(create_time,'%%e')"}).values('create_time') \
#     .annotate(send_num=Count('create_time')).values('create_time')
#
#
#
# #当前日期格式
# cur_date = datetime.datetime.now().date()
# #前一天日期
# yester_day = cur_date - datetime.timedelta(days=1)
# #前一周日期
# week = cur_date - datetime.timedelta(days=30)
#
#
# #查询前一周数据,也可以用range,我用的是glt,lte大于等于
# obj_list=ApiCase.objects.filter(create_time__gte=week, create_time__lte=cur_date)
# print(obj_list)
#
# c  = "2020-04-02 14:49:07,494 - INFO: 用例ID:7↵2020-04-02 14:49:07,497 - INFO: 请求方式:2↵2020-04-02 14:49:07,499 - INFO: 请求url:http://api.dlab.com/app/user/login/v2↵2020-04-02 14:49:07,500 - INFO: 请求headers:{'Content-Type': 'application/json', 'api-version': 'v1.2.0', 'request-source': 'web', 'authorization': '${data.token}'}↵2020-04-02 14:49:07,500 - INFO: 请求参数:{'mobile': '17671105406', 'password': 'yuanman99'}↵2020-04-02 14:49:07,655 - INFO: 响应结果:{'flag': True, 'msg': 'success', 'code': 0, 'data': {'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjo0ODc4NzU4LCJleHAiOjE1ODY0MTQ5NDcsImlhdCI6MTU4NTgxMDE0N30.8bWuEkH42_4OgBNw-S8WpbE0juntMf6aOejmME55qqk', 'uid': 4878758}}↵2020-04-02 14:49:07,656 - INFO: 校验方式:json_response↵2020-04-02 14:49:07,656 - INFO: 校验值[{'key': '$.code', 'value': '0', 'initiate': true}]"
#
# s_replace = c.replace('↵', '</br>',)
# print(s_replace)




import os
from git.repo import Repo
from git.repo.fun import is_git_dir


# class GitRepository(object):
#     """
#     git仓库管理
#     """
#     def __init__(self, local_path, repo_url, branch='master'):
#         self.local_path = local_path
#         self.repo_url = repo_url
#         self.repo = None
#         self.initial(repo_url, branch)
#
#     def initial(self, repo_url, branch):
#         """
#         初始化git仓库
#         :param repo_url:
#         :param branch:
#         :return:
#         """
#         if not os.path.exists(self.local_path):
#             os.makedirs(self.local_path)
#
#         git_local_path = os.path.join(self.local_path, '.git')
#         if not is_git_dir(git_local_path):
#             self.repo = Repo.clone_from(repo_url, to_path=self.local_path, branch=branch)
#         else:
#             self.repo = Repo(self.local_path)
#
#     def pull(self):
#         """
#         从线上拉最新代码
#         :return:
#         """
#         self.repo.git.pull()
#
#     def branches(self):
#         """
#         获取所有分支
#         :return:
#         """
#         branches = self.repo.remote().refs
#         return [item.remote_head for item in branches if item.remote_head not in ['HEAD', ]]
#
#     def commits(self):
#         """
#         获取所有提交记录
#         :return:
#         """
#         commit_log = self.repo.git.log('--pretty={"commit":"%h","author":"%an","summary":"%s","date":"%cd"}',
#                                        max_count=50,
#                                        date='format:%Y-%m-%d %H:%M')
#         log_list = commit_log.split("\n")
#         return [eval(item) for item in log_list]
#
#     def tags(self):
#         """
#         获取所有tag
#         :return:
#         """
#         return [tag.name for tag in self.repo.tags]
#
#     def change_to_branch(self, branch):
#         """
#         切换分值
#         :param branch:
#         :return:
#         """
#         self.repo.git.checkout(branch)
#
#     def change_to_commit(self, branch, commit):
#         """
#         切换commit
#         :param branch:
#         :param commit:
#         :return:
#         """
#         self.change_to_branch(branch=branch)
#         self.repo.git.reset('--hard', commit)
#
#     def change_to_tag(self, tag):
#         """
#         切换tag
#         :param tag:
#         :return:
#         """
#         self.repo.git.checkout(tag)

import requests,json,sqlite3,uuid

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
}
#gitlab地址
git_url='https://github.com/2295256562'
#gitlab的token
git_token='d96f58168bafd41d56bccecf3c02d9bee11a1494'

session = requests.Session()
headers['PRIVATE-TOKEN']=git_token
session.headers = headers
git_login=session.get(git_url,headers=headers)


import gitlab
client = gitlab.Gitlab("https://github.com/2295256562", private_token='51164531276d36c30642ca547112df70b022297b', timeout=8000)
client.auth()
project = client.projects.get('python')
commits = project.commits.list(ref_name='master', page=0, per_page=20)
print(commits)
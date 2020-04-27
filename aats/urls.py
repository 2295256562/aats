"""aats URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve

from Users.views import RegUserView
from aats import settings
from product.views import ProjectListView, ProjectAddView, ProjectGetView, sourceListView, AddModelView, ListModel, \
    SendRequest, projectgetModel, addApicase, ListApiCase, GETCaseInfo, TestTask, HeadersView, HeadersinfoView, \
    reportView, timeTask, TimeTaskList, listCase, HeadersFilterView, CaseReportInfo, statisticseveryday
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('admin/', admin.site.urls),
    # re_path("api_auth", include("rest_framework.urls")),

    # 用户
    path('api/v1/login/', obtain_jwt_token),
    path('api/v1/reg/', RegUserView.as_view({'post': 'create'})),
    path('api/v1/count/', statisticseveryday.as_view()),
    re_path('media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

    # 项目
    path('api/v1/add_project/', ProjectAddView.as_view()),
    path('api/v1/project_list/', ProjectListView.as_view({'get': 'list'})),
    re_path('api/v1/u_project/(?P<pk>\d+)/', ProjectListView.as_view({'put': 'update'})),
    re_path('api/v1/project_info/(?P<pk>\d+)/', ProjectGetView.as_view({'get': 'retrieve'})),
    re_path('api/v1/del/(?P<pk>\d+)/', ProjectListView.as_view({'delete': 'destroy'})),

    # 模块
    re_path('api/v1/ListProject', sourceListView.as_view()),
    re_path('api/v1/AddModel', AddModelView.as_view({'post': 'create'})),
    re_path('api/v1/modelList', ListModel.as_view({'get': 'list'})),
    re_path('api/v1/delMod/(?P<pk>\d+)/', ListModel.as_view({'delete': 'destroy'})),
    re_path('api/v1/modelInfo/(?P<pk>\d+)/', ListModel.as_view({'get': 'retrieve'})),
    re_path('api/v1/updateMod/(?P<pk>\d+)/', ListModel.as_view({'put': 'update'})),

    # 接口调试
    re_path('api/v1/send', SendRequest.as_view()),
    # 通过项目id查询所有模块
    re_path('api/v1/allModel/(?P<project_id_id>\d+)', projectgetModel.as_view()),
    re_path('api/v1/addApiCase', addApicase.as_view()),
    # 接口测试用例列表
    re_path('api/v1/ListApicase', ListApiCase.as_view({'get': 'list'})),
    # 接口用例详情
    re_path('api/v1/apicase_info/(?P<pk>\d+)/', GETCaseInfo.as_view({'get': 'retrieve'})),
    re_path('api/v1/caselist/', listCase.as_view()),
    re_path('api/v1/updateCase/(?P<pk>\d+)/', GETCaseInfo.as_view({'put': 'update'})),

    # 执行测试任务接口
    re_path('api/v1/testTask/', TestTask.as_view()),

    # 请求头管理列表
    re_path('api/v1/headerslist/', HeadersView.as_view({'get': 'list'})),
    re_path('api/v1/headersinfo/(?P<pk>\d+)/', HeadersinfoView.as_view({'get': 'retrieve'})),
    re_path('api/v1/updateHeaders/(?P<pk>\d+)/', HeadersinfoView.as_view({'put': 'update'})),
    re_path('api/v1/Filterheader/', HeadersFilterView.as_view({'get': 'list'})),

    # 接口报告列表
    re_path('api/v1/ReportList/', reportView.as_view({'get': 'list'})),
    re_path('api/v1/Reportinfo/(?P<pk>\d+)/', reportView.as_view({'get': 'retrieve'})),
    re_path('api/v1/caseReport/', CaseReportInfo.as_view({'get': 'list'})),

    # re_path('api/v1/task/', timedTaskView.as_view({'get': 'list', 'post': 'create'})),

    # 定时任务
    re_path('api/v1/addTimeTask/', timeTask.as_view()),
    re_path('api/v1/TimeTaskList/', TimeTaskList.as_view({'get': 'list'})),
    re_path('api/v1/TaskInfo/(?P<pk>\d+)', TimeTaskList.as_view({'get': 'retrieve'})),
]

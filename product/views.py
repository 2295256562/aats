import json
import logging
from json import dumps

from django.db.models import Count
from rest_framework.response import Response
from rest_framework.views import APIView
from myCelery.run_case.tasks import run_test, getApi
from Users.custompage import CustomPagination
from product.models import Project, Model, ApiCase, Headers, Report, APIcaseinfo, API
from product.serializer import ListProjectSerializer, AddProjectSerializer, SoureceProjectSer, AddModelSer, \
    ListModelSer, modelSerializer, addAPicaseSer, listApiCase, GETinfoSer, HeadersSer, HeadersInfoSer, reportinfoSer, \
    timeTaskSer, HeadersfilterSer, caseReportInfoSer
from utils.api.httpServer import httpservice
from utils.baseViewSet import BaseViewSet
from utils.baseresponse import BaseResponse
from utils.caseNumber import get_pinyin_first_alpha

logger = logging.getLogger('mdjango')


class ProjectListView(BaseViewSet):
    queryset = Project.objects.all().order_by('-id')
    serializer_class = ListProjectSerializer
    pagination_class = CustomPagination
    # filter_fields = ('project_name',)
    search_fields = ('project_name',)

    """项目列表接口"""

    def get(self, request):
        return self.list(request)

    def update(self, request, *args, **kwargs):
        """
        put /entity/{pk}/
        """
        instance = self.get_object()
        data = request.data
        data['project_address'] = dumps(data['project_address'], ensure_ascii=False)
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return BaseResponse(data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        project_id = instance.__dict__['id']
        # 通过项目id查询是否有用例数据;如果有数据项目就不能删除,否则则可以
        obj = ApiCase.objects.filter(project_id_id=project_id)
        if obj:
            data = {"code": "000002", "message": "失败", "data": "项目下有测试数据不能删除"}
        else:
            Headers.objects.update(is_deleted=1)
            self.perform_destroy(instance)
            data = {"code": "000000", "message": "成功", "data": "数据删除成功"}
        return Response(data)


class ProjectAddView(APIView):
    """
    新增项目
    """

    def post(self, request):
        user_data = request.data
        data = {}
        print(user_data)
        project_address = dumps(user_data['project_address'], ensure_ascii=False)
        data = {
            'project_name': user_data['project_name'],
            'project_address': project_address,
            'document': user_data['document']
        }
        ser = AddProjectSerializer(data=data, context={'request': request})
        ser.is_valid(raise_exception=True)
        ser.save()

        # 获取swagger文档
        getApi.delay(user_data['document'], user_data['project_name'], ser.data['id'])
        # 获取项目名称写入headers表
        # data['project_name']
        print(ser.data)
        headers = [{"headerSetKey": "Content-Type", "headersSetValue": "application/json", "headersStatus": True}]

        h_data = {
            'project_name': data['project_name'],
            'project': ser.data['id'],
            'headers': dumps(headers, ensure_ascii=False)
        }
        sh = HeadersSer(data=h_data, context={'request': request})
        sh.is_valid(raise_exception=True)
        sh.save()
        return Response({"code": "000000", "message": "成功", "data": ser.data})


class ProjectGetView(BaseViewSet):
    queryset = Project.objects.all().order_by('-id')
    serializer_class = ListProjectSerializer

    def get(self, request, pk):
        return self.retrieve(Project.objects.get(pk=pk))


class HeadersView(BaseViewSet):
    queryset = Headers.objects.all().order_by("-id")
    serializer_class = HeadersSer
    pagination_class = CustomPagination
    # filter_fields = ('project', 'project_name')
    # search_fields = ('project_id', 'project_name')


class HeadersFilterView(BaseViewSet):
    queryset = Headers.objects.all().order_by("-id")
    serializer_class = HeadersfilterSer
    pagination_class = CustomPagination
    search_fields = ('project_name',)


class HeadersinfoView(BaseViewSet):
    queryset = Headers.objects.all()
    serializer_class = HeadersInfoSer

    def update(self, request, *args, **kwargs):
        """
        put /entity/{pk}/
        """
        instance = self.get_object()
        data = request.data
        data['headers'] = dumps(data['headers'], ensure_ascii=False)
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return BaseResponse(data=serializer.data)


class sourceListView(APIView):

    def get(self, request):
        products = Project.objects.all()
        ser = SoureceProjectSer(products, many=True)
        return Response({"code": "000000", "message": "成功", "data": ser.data})


class AddModelView(BaseViewSet):
    queryset = Model.objects.all().order_by("-id")
    serializer_class = AddModelSer


class ListModel(BaseViewSet):
    queryset = Model.objects.all().order_by("-id")
    serializer_class = ListModelSer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        model_id = instance.__dict__['project_id_id']
        print(model_id)
        # 通过项目id查询是否有用例数据;如果有数据项目就不能删除,否则则可以
        obj = ApiCase.objects.filter(project_id_id=model_id)
        if obj:
            data = {"code": "000002", "message": "失败", "data": "项目下有测试数据不能删除"}
        else:
            Headers.objects.update(is_deleted=1)
            self.perform_destroy(instance)
            data = {"code": "000000", "message": "成功", "data": "数据删除成功"}
        return Response(data)


# 调试接口测试
class SendRequest(APIView):

    def post(self, request):
        data = request.data
        print(data)
        params = data['params']
        if data['type'] != 2:
            params = {x['key']: x['value'] for x in params}

        headers = {i['headerSetKey']: i['headersSetValue'] for i in data['headers']}

        if data['method'] == '1':
            if data['type'] == 1: Type = 'params'

        if data['method'] == '2':
            if data['type'] == 1: Type = 'x-www-form-urlencoded'
            if data['type'] == 2: Type = 'json'
            if data['type'] == 3: Type = 'form-data'
        # print(data['checkType'])
        # print(data['checkText'])
        # print(data['method'])
        # print(data['url'])
        # print(params)
        resp = httpservice(data['method'], data['url'], data['type'], params, headers)
        Responses = resp.request()
        if Responses.status_code == 200:
            print(data['checkText'])
            check = resp.checkRequest(data['checkType'], data['checkText'])
            return Response({"code": "000000", "message": "成功", "data": Responses.json(), 'check': check})
        return Response({"code": "000000", "message": "成功", "data": Responses.json(), 'check': '失败'})


# 项目id查询模块
class projectgetModel(APIView):

    def get(self, request, project_id_id):
        models = Model.objects.filter(project_id_id=project_id_id)
        ser = modelSerializer(models, many=True)
        return Response({"code": "000000", "message": "成功", "data": ser.data})


class addApicase(APIView):

    def post(self, request):
        data = request.data
        # print(data)
        data['params'] = dumps(data['params'], ensure_ascii=False)
        data['checkText'] = dumps(data['checkText'], ensure_ascii=False)
        ser = addAPicaseSer(data=data, context={'request': request})
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response({"code": "000000", "message": "成功", "data": ser.data})


class ListApiCase(BaseViewSet):
    queryset = ApiCase.objects.all().order_by("-id")
    serializer_class = listApiCase
    # filter_backends = (filters.SearchFilter,)
    search_fields = ('case_name',)
    filter_fields = ('project_id', 'id', 'url', 'case_name')


class listCase(APIView):

    def get(self, request):
        user_data = request.GET.getlist('id')
        print(user_data)
        data = ApiCase.objects.filter(pk__in=user_data)
        print(data)
        ser = listApiCase(data, many=True)
        return Response({"code": "000000", "message": "成功", "data": ser.data})


class GETCaseInfo(BaseViewSet):
    queryset = ApiCase.objects.all()
    serializer_class = GETinfoSer

    def update(self, request, *args, **kwargs):
        """
        put /entity/{pk}/
        """
        instance = self.get_object()
        data = request.data
        data['params'] = dumps(data['params'], ensure_ascii=False)
        data['checkText'] = dumps(data['checkText'], ensure_ascii=False)
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return BaseResponse(data=serializer.data)


class reportView(BaseViewSet):
    queryset = Report.objects.all().order_by('-id')
    serializer_class = reportinfoSer
    pagination_class = CustomPagination


class CaseReportInfo(BaseViewSet):
    queryset = APIcaseinfo.objects.all()
    serializer_class = caseReportInfoSer
    filter_fields = ('case_report',)


class TestTask(APIView):

    # 发起测试任务
    def post(self, request):
        # 1. 获取用户的请求数据
        user_data = request.data
        # logger.info(user_data)
        # 2. 判断用户传过来的id个数组长度是否大于1, 如果大于1就返回任务编号,任务由后台执行
        # if len((user_data['ids'])) > 1:
        env = {x['envName']: x['envAddres'] for x in user_data['envname']}
        new_env = {v: k for k, v in env.items()}
        envname = new_env[user_data['env']]
        # print(list(new_env)[0])
        # 2.1 调生成任务编号方法,生成编号,并返回给前端
        TaskNo = get_pinyin_first_alpha(user_data['project_name'])
        # 插入任务编号到接口报告表
        report = Report(R_Number=TaskNo, R_Env=envname, R_CaseSum=len(user_data['ids']), create_user=request.user,
                        R_project=user_data['project_name'], R_CaseId=user_data['ids'], R_Type=1)
        report.save()
        # 调后台celery任务
        run_test.delay(TaskNo, user_data['ids'], user_data['projectid'], list(new_env)[0])
        # 返回任务编号
        return Response({"code": "000000", "message": "成功", "data": TaskNo})
    # else:
    # 返回执行结果
    # obj = ApiCase.objects.values().get(pk=user_data['ids'])
    # print(obj)
    # return Response({"code": "000000", "message": "成功", "data": {}})


# from django_celery_beat.models import PeriodicTask  # 倒入插件model

#
# class timedTaskView(BaseViewSet):
#     queryset = PeriodicTask.objects.all().order_by('-id')
#     serializer_class = timeTaskSer
#     pagination_class = CustomPagination

#
# class taskName(APIView):
#     def get(self, request):
#         # return Response({})
#         return Response({"code": "000000", "message": "成功", "data": data})

from djcelery.models import CrontabSchedule, PeriodicTask


class timeTask(APIView):

    def post(self, request):
        data = request.data
        env = {x['envName']: x['envAddres'] for x in data['envname']}
        new_env = {v: k for k, v in env.items()}
        envname = new_env[data['env']]
        projectname = Project.objects.get(pk=data['project'])
        TaskNo = get_pinyin_first_alpha("定时任务")

        # 创建测试报告
        Report.objects.create(R_Number=TaskNo, R_Env=envname, R_CaseSum=len(data['caseList']),
                              create_user=request.user, R_CaseId=data['caseList'], R_project=projectname)

        if data['task'] == '每天':
            re = data['time'].split(':')
            try:
                cron = CrontabSchedule.objects.get_or_create(minute=re[1], hour=int(re[0]) - 8, day_of_week='*',
                                                             day_of_month='*',
                                                             month_of_year='*')
            except:
                logger.error("任务时间已存在不可重复创建")
        elif data['task'] == '每周':
            re = data['time'].split(':')
            try:
                cron = CrontabSchedule.objects.create(minute=re[1], hour=int(re[0]) - 8, day_of_week=data['week'],
                                                      day_of_month='*',
                                                      month_of_year='*')
            except:
                logger.error("任务时间已存在不可重复创建")
        else:
            re = data['time'].split(" ")
            try:
                cron = CrontabSchedule.objects.create(minute=re[0], hour=int(re[1]) - 8, day_of_week=re[2],
                                                      day_of_month=re[3],
                                                      month_of_year=re[4])
            except:
                logger.error("任务时间已存在不可重复创建")
        try:
            args = [TaskNo, data['caseList'], data['project'], data['env']]
            PeriodicTask.objects.get_or_create(name=data["name"], task='run_test', crontab=cron,
                                               args=json.dumps(args), description=data['desc'])
        except:
            return Response({"code": "000002", "message": "失败", "data": "任务名称不可重复"})
        return Response({"code": "000000", "message": "成功", "data": "任务创建成功"})


class TimeTaskList(BaseViewSet):
    queryset = PeriodicTask.objects.all().order_by('-id')
    serializer_class = timeTaskSer
    pagination_class = CustomPagination


class statisticseveryday(APIView):

    def get(self, request):
        # 最近新增case
        from django.db import connection

        cursor = connection.cursor()

        cursor.execute("select b.days,IFNULL(c.c,0) from (SELECT @cdate := date_add(@cdate,interval -1 day) days from (SELECT @cdate := CURDATE() from API limit 30) t1 ) b left join  (select  count(1) as c  ,date from  (SELECT DATE_FORMAT(  u.create_time , '%Y-%m-%d' ) AS date  FROM API AS u WHERE( u.create_time + INTERVAL 30 Day)  > now()) a group by a.date ) c on b.days =c.date ORDER BY b.days")
        RECENTLYADDCASE = cursor.fetchall()
        list = []
        for row in RECENTLYADDCASE:

            dic = {"count": row[1], "create_time": row[0]}
            list.append(dic)

        # 用例总数
        CASESUM = ApiCase.objects.count()

        # 项目总数
        PROJECTSUM = Project.objects.count()

        # 定时任务总数
        TimerTask = PeriodicTask.objects.count()

        obj = {
            "RECENTLYADDCASE": list,
            "CASESUM": CASESUM,
            "PROJECTSUM": PROJECTSUM,
            "TimerTask": TimerTask
        }

        return Response({"code": "000000", "message": "成功", "data": obj})


class APilist(APIView):

    def get(self, request):
        ca_num = API.objects.values('tag').all().distinct()
        list = []
        for i in ca_num:
            dict = {}
            da = API.objects.values().filter(tag=i['tag'])
            dict['label'] = da
            ll = {}
            ll[i['tag']] = da
            list.append(ll)
        return Response({"code": "000000", "message": "成功", "data":list})
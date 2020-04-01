import json

from rest_framework import serializers
from .models import *


class AddProjectSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    create_user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Project
        fields = '__all__'  # 返回所有字段


class HeadersfilterSer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    create_user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Headers
        fields = '__all__'  # 返回所有字段

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['headers'] = json.loads(data['headers'])
        # data['headers'] = {x['headerSetKey']: x['headersSetValue'] for x in headers}
        # data['headers'] = str(data['headers'])
        # 返回处理之后的数据
        return data


class HeadersSer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    create_user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Headers
        fields = '__all__'  # 返回所有字段

    def to_representation(self, instance):
        data = super().to_representation(instance)
        headers = json.loads(data['headers'])
        data['headers'] = {x['headerSetKey']: x['headersSetValue'] for x in headers}
        data['headers'] = str(data['headers'])
        # 返回处理之后的数据
        return data


class HeadersInfoSer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    create_user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Headers
        fields = '__all__'  # 返回所有字段

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['headers'] = json.loads(data['headers'])
        # data['headers'] = {x['headerSetKey']: x['headersSetValue'] for x in headers }
        # data['headers'] = str(data['headers'])
        # 返回处理之后的数据
        return data


class ListProjectSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'  # 返回所有字段

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['project_address'] = json.loads(data['project_address'])
        # 返回处理之后的数据
        return data


class SoureceProjectSer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['project_name', 'id']


class AddModelSer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Model
        fields = '__all__'  # 返回所有字段


class ListModelSer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    # project_name = serializers.CharField(source='project_id.project_name')
    project_name = serializers.CharField(source='project_id.project_name')

    # project_name = serializers.ReadOnlyField()
    # model_name = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Model
        fields = '__all__'


class modelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ['id', 'model_name']


class addAPicaseSer(serializers.ModelSerializer):
    create_user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = ApiCase
        fields = '__all__'


class listApiCase(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    update_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    project_name = serializers.CharField(source='project_id.project_name')

    class Meta:
        model = ApiCase
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['params'] = str(json.loads(data['params']))
        # 返回处理之后的数据
        return data


class GETinfoSer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    update_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    project_name = serializers.CharField(source='project_id.project_name')

    class Meta:
        model = ApiCase
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['params'] = json.loads(data['params'])
        data['checkText'] = json.loads(data['checkText'])
        # 返回处理之后的数据
        return data


class reportinfoSer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = Report
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['R_CaseId'] = json.loads(data['R_CaseId'])
        return data


class caseReportInfoSer(serializers.ModelSerializer):
    class Meta:
        model = APIcaseinfo
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # cc = json.dumps(data['case_headers'])
        # data['case_headers'] = json.loads(data['case_headers'])
        print(type(data['case_headers']))
        print(data['case_headers'])
        print(type(eval(data['case_headers'])))
        data['case_headers'] = eval(data['case_headers'])
        data['case_params'] = eval(data['case_params'])
        data['case_response'] = eval(data['case_response'])
        return data



from djcelery.models import CrontabSchedule, PeriodicTask


class timeTaskSer(serializers.ModelSerializer):
    date_changed = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = PeriodicTask
        fields = '__all__'
        depth = 1

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['args'] = json.loads(data['args'])
        print(type(data['args'][2]))
        project = Project.objects.get(pk=data['args'][2])
        print(project.project_address)
        env = {x['envName']: x['envAddres'] for x in eval(project.project_address)}
        # new_env = {v: k for k, v in env.items()}
        # data['args'][3] = env[data['args'][3]]
        # print(type(list(project.project_address)))
        print(env)
        # data['args'][3] =
        data['crontab']['hour'] = int(data['crontab']['hour']) + 8
        # 返回处理之后的数据
        return data

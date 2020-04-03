
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
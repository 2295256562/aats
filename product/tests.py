import datetime
import os, django
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aats.settings")
from django.test import TestCase
import json
# # Create your tests here.
# list = ['sfwf', [2,3,4], 35, 'fsf']
# print(list)
# c = (json.dumps(list))
# print(json.loads(c))
# from product.models import Project

# print(dt.strftime('%Y-
print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

# Generated by Django 2.2.8 on 2020-03-14 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20200314_1013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='R_Type',
            field=models.IntegerField(choices=[(1, '即时任务'), (2, '定时任务')], default=2, verbose_name='任务类型'),
        ),
    ]

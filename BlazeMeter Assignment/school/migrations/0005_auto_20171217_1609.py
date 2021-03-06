# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-12-17 14:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0004_auto_20171215_1439'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='grade',
            options={'ordering': ('grade',)},
        ),
        migrations.AlterField(
            model_name='student',
            name='email',
            field=models.EmailField(max_length=75),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='email',
            field=models.EmailField(max_length=75),
        ),
    ]

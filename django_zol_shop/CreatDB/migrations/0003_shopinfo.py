# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-10-04 07:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CreatDB', '0002_auto_20191004_1134'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='名字')),
                ('introduction', models.CharField(max_length=256, verbose_name='商品简介')),
                ('price', models.IntegerField(verbose_name='价格')),
                ('inventory', models.IntegerField(verbose_name='库存')),
                ('kind', models.TextField(verbose_name='种类')),
                ('sales', models.IntegerField(verbose_name='销量')),
                ('Image', models.ImageField(upload_to='', verbose_name='图片')),
            ],
        ),
    ]

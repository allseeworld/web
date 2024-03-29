# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-10-06 02:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zol_index', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop_show',
            name='shop_id1',
            field=models.IntegerField(default=0, verbose_name='商品id1'),
        ),
        migrations.AlterField(
            model_name='shop_show',
            name='shop_id2',
            field=models.IntegerField(default=0, verbose_name='商品id2'),
        ),
        migrations.AlterField(
            model_name='shop_show',
            name='shop_id3',
            field=models.IntegerField(default=0, verbose_name='商品id3'),
        ),
        migrations.AlterField(
            model_name='shop_show',
            name='shop_id4',
            field=models.IntegerField(default=0, verbose_name='商品id4'),
        ),
        migrations.AlterField(
            model_name='shop_show',
            name='shop_id5',
            field=models.IntegerField(default=0, verbose_name='商品id5'),
        ),
        migrations.AlterField(
            model_name='shop_show',
            name='shop_id6',
            field=models.IntegerField(default=0, verbose_name='商品id6'),
        ),
        migrations.AlterField(
            model_name='shop_show',
            name='shop_id7',
            field=models.IntegerField(default=0, verbose_name='商品id7'),
        ),
        migrations.AlterField(
            model_name='shop_show',
            name='shop_id8',
            field=models.IntegerField(default=0, verbose_name='商品id8'),
        ),
        migrations.AlterField(
            model_name='shop_show',
            name='shop_id9',
            field=models.IntegerField(default=0, verbose_name='商品id9'),
        ),
        migrations.AlterField(
            model_name='shop_show',
            name='show_name',
            field=models.CharField(default='', max_length=64, verbose_name='展示区的名字'),
        ),
        migrations.AlterField(
            model_name='shop_show',
            name='type_id1',
            field=models.IntegerField(default=0, verbose_name='商品大类id1'),
        ),
        migrations.AlterField(
            model_name='shop_show',
            name='type_id2',
            field=models.IntegerField(default=0, verbose_name='商品大类id2'),
        ),
        migrations.AlterField(
            model_name='shop_show',
            name='type_id3',
            field=models.IntegerField(default=0, verbose_name='商品大类id3'),
        ),
    ]

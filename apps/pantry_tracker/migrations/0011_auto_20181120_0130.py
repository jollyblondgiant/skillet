# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-11-20 01:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pantry_tracker', '0010_merge_20181120_0103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grocerylist',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_grocery_list', to='pantry_tracker.Product'),
        ),
    ]

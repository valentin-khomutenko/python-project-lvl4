# Generated by Django 3.1.7 on 2021-04-01 05:33
from typing import Any, List

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies: List[Any] = []

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField()),
            ],
        ),
    ]

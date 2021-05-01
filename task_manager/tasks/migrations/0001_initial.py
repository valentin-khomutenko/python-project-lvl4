# Generated by Django 3.1.7 on 2021-05-01 18:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('statuses', '0003_auto_20210401_0550'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,
                 related_name='author', to=settings.AUTH_USER_MODEL)),
                ('executor', models.ForeignKey(blank=True, null=True,
                                               on_delete=django.db.models.deletion.PROTECT,
                 related_name='executor', to=settings.AUTH_USER_MODEL)),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,
                                             to='statuses.status')),
            ],
        ),
    ]

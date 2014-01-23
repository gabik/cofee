# encoding: utf8
from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):
    
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='branch_profile',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field=u'id', unique=True)),
                ('phone_num', models.CharField(max_length=30, null=True, blank=True)),
                ('address', models.CharField(max_length=50, null=True, blank=True)),
                ('hash', models.CharField(max_length=100, null=True, blank=True)),
                ('header', models.CharField(max_length=300, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='client_profile',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field=u'id', unique=True)),
                ('phone_num', models.CharField(max_length=30, null=True, blank=True)),
                ('hash', models.CharField(max_length=100, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

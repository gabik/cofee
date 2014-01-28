# encoding: utf8
from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):
    
    dependencies = [
        ('orders', '0002_auto_20140128_1102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client_orders',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field=u'id'),
        ),
    ]

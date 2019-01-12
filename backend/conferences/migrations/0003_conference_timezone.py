# Generated by Django 2.1.5 on 2019-01-12 15:56

from django.db import migrations
import timezone_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('conferences', '0002_auto_20181229_1249'),
    ]

    operations = [
        migrations.AddField(
            model_name='conference',
            name='timezone',
            field=timezone_field.fields.TimeZoneField(default='Europe/Rome'),
            preserve_default=False,
        ),
    ]

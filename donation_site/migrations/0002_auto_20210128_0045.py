# Generated by Django 3.1.1 on 2021-01-27 18:45

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('donation_site', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='text',
            new_name='description',
        ),
        migrations.RemoveField(
            model_name='post',
            name='published_date',
        ),
        migrations.AddField(
            model_name='post',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 27, 18, 44, 52, 246915, tzinfo=utc)),
        ),
    ]

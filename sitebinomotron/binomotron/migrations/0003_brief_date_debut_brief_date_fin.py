# Generated by Django 4.1.3 on 2022-11-17 17:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('binomotron', '0002_remove_apprenant_pub_date_remove_brief_pub_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='brief',
            name='date_debut',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 17, 17, 56, 46, 83012, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AddField(
            model_name='brief',
            name='date_fin',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 17, 17, 56, 46, 83504, tzinfo=datetime.timezone.utc)),
        ),
    ]

# Generated by Django 4.1.3 on 2022-11-18 10:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('binomotron', '0006_alter_apprenant_nom_alter_apprenant_prenom_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brief',
            name='date_debut',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 18, 10, 7, 5, 945191, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='brief',
            name='date_fin',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 18, 10, 7, 5, 945228, tzinfo=datetime.timezone.utc)),
        ),
    ]

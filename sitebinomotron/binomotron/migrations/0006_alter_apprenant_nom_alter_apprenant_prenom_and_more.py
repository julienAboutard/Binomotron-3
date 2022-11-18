# Generated by Django 4.1.3 on 2022-11-18 09:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('binomotron', '0005_alter_brief_date_debut_alter_brief_date_fin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apprenant',
            name='nom',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='apprenant',
            name='prenom',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='brief',
            name='date_debut',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 18, 9, 34, 54, 406200, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='brief',
            name='date_fin',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 18, 9, 34, 54, 406263, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='brief',
            name='lien',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='brief',
            name='nom',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='groupe',
            name='nom',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
# Generated by Django 4.1.3 on 2022-11-18 13:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('binomotron', '0008_alter_brief_date_debut_alter_brief_date_fin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brief',
            name='nombre',
            field=models.PositiveIntegerField(default=2, validators=[django.core.validators.MinValueValidator(2)]),
        ),
    ]

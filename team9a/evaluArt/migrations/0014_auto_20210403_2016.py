# Generated by Django 2.2.17 on 2021-04-03 20:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evaluArt', '0013_auto_20210403_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='number',
            field=models.IntegerField(default=5, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)]),
        ),
    ]
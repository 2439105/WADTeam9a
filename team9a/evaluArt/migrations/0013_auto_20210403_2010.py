# Generated by Django 2.2.17 on 2021-04-03 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evaluArt', '0012_auto_20210403_1951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='number',
            field=models.IntegerField(),
        ),
    ]

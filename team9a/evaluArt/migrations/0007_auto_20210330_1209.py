# Generated by Django 2.2.17 on 2021-03-30 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evaluArt', '0006_userprofile_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]

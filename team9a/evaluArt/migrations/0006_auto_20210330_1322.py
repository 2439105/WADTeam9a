# Generated by Django 2.2.17 on 2021-03-30 12:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('evaluArt', '0005_auto_20210328_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='artwork',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='artwork', to='evaluArt.Artwork'),
        ),
        migrations.AlterField(
            model_name='comments',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='evaluArt.UserProfile'),
        ),
    ]

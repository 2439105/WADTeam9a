# Generated by Django 2.2.17 on 2021-03-24 18:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('evaluArt', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artwork',
            fields=[
                ('artwork_id', models.IntegerField(primary_key=True, serialize=False)),
                ('picture', models.ImageField(upload_to='')),
                ('description', models.CharField(max_length=800)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evaluArt.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('artwork', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evaluArt.Artwork')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evaluArt.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('artwork', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evaluArt.Artwork')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evaluArt.UserProfile')),
            ],
        ),
    ]

# Generated by Django 5.2 on 2025-04-24 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('url', models.URLField()),
                ('artista', models.CharField(max_length=100)),
                ('canal', models.CharField(max_length=100)),
                ('duracao_segundos', models.IntegerField()),
                ('data_cadastro', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'video',
            },
        ),
    ]

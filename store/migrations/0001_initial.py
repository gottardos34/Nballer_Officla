# Generated by Django 4.0.1 on 2022-01-24 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_match', models.CharField(max_length=20, unique=True)),
                ('date', models.CharField(max_length=20)),
                ('home', models.CharField(max_length=30)),
                ('visitor', models.CharField(max_length=30)),
            ],
        ),
    ]

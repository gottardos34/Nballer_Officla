# Generated by Django 4.0.1 on 2022-01-26 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_match_id_match'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='code',
            field=models.CharField(default=0, max_length=5),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='team',
            name='surname',
            field=models.CharField(max_length=20),
        ),
    ]

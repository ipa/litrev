# Generated by Django 3.0.4 on 2020-03-26 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('screening', '0006_auto_20200324_1706'),
    ]

    operations = [
        migrations.AddField(
            model_name='pubmedimportedarticle',
            name='landmark',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]

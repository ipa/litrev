# Generated by Django 3.0.4 on 2020-03-24 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tagging', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TagGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=25)),
            ],
        ),
    ]

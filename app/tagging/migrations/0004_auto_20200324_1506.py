# Generated by Django 3.0.4 on 2020-03-24 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tagging', '0003_auto_20200324_1502'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='tag_group',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='tagging.TagGroup'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='taggroup',
            name='enabled',
            field=models.BooleanField(default=False),
        ),
    ]
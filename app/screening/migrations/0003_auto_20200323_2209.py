# Generated by Django 3.0.4 on 2020-03-23 21:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('screening', '0002_remove_pubmedimportedarticle_doi'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pubmedimportedarticle',
            old_name='import_id',
            new_name='pmimport',
        ),
        migrations.RenameField(
            model_name='screeningstatus',
            old_name='article_id',
            new_name='article',
        ),
    ]

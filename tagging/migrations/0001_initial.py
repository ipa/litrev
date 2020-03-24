# Generated by Django 3.0.4 on 2020-03-24 12:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('screening', '0004_auto_20200323_2216'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='ArticleTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='screening.PubmedImportedArticle')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tagging.Tag')),
            ],
        ),
    ]

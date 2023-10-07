# Generated by Django 3.2.22 on 2023-10-06 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapping', '0004_remove_informations_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='informations',
            name='name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='informations',
            name='release_date',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='pages',
            name='name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]

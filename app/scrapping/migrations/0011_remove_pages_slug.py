# Generated by Django 3.2.23 on 2023-11-30 13:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrapping', '0010_informations_image_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pages',
            name='slug',
        ),
    ]

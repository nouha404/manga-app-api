# Generated by Django 3.2.22 on 2023-10-06 16:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrapping', '0006_alter_informations_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='informations',
            name='name',
        ),
    ]
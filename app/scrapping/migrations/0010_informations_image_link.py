# Generated by Django 3.2.23 on 2023-11-30 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapping', '0009_auto_20231129_2338'),
    ]

    operations = [
        migrations.AddField(
            model_name='informations',
            name='image_link',
            field=models.TextField(default='unknown'),
        ),
    ]
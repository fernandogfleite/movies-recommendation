# Generated by Django 4.0.2 on 2022-02-03 18:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='movierating',
            options={'ordering': ('movie', 'rating')},
        ),
    ]

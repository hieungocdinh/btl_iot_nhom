# Generated by Django 4.2.5 on 2024-11-08 05:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='trashcompartment',
            unique_together={('id_trash_can', 'label')},
        ),
    ]

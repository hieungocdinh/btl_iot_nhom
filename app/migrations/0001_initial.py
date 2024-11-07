# Generated by Django 4.2.5 on 2024-11-07 17:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TrashCan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TrashCompartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empty_count', models.IntegerField(default=0)),
                ('lable', models.CharField(max_length=255)),
                ('max_quantity', models.IntegerField(default=20)),
                ('id_trash_can', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.trashcan')),
            ],
        ),
        migrations.CreateModel(
            name='Trash',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trash_img_url', models.URLField()),
                ('trash_img_public_id', models.CharField(max_length=255)),
                ('date', models.DateTimeField()),
                ('quantity', models.IntegerField()),
                ('id_trash_can', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.trashcan')),
                ('id_trash_compartment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.trashcompartment')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

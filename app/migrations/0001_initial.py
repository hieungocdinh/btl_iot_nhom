# Generated by Django 4.2.5 on 2024-11-09 05:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TrashArea',
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
                ('label', models.CharField(max_length=255)),
                ('max_quantity', models.IntegerField(default=20)),
                ('id_trash_area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.trasharea')),
            ],
            options={
                'unique_together': {('id_trash_area', 'label')},
            },
        ),
        migrations.CreateModel(
            name='Trash',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trash_img_url', models.URLField()),
                ('trash_img_public_id', models.CharField(max_length=255)),
                ('date', models.DateTimeField()),
                ('quantity', models.IntegerField()),
                ('id_trash_area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.trasharea')),
                ('id_trash_compartment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.trashcompartment')),
            ],
        ),
    ]

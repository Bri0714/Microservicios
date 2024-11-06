# Generated by Django 4.2 on 2024-11-02 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ruta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ruta_nombre', models.CharField(max_length=50, unique=True, verbose_name='Nombre de la Ruta')),
                ('ruta_movil', models.IntegerField(unique=True, verbose_name='Numero Movil')),
                ('instituciones_ids', models.JSONField(default=list, verbose_name='IDs de Instituciones Asociadas')),
                ('activa', models.BooleanField(default=True, verbose_name='Estado')),
                ('user_id', models.IntegerField()),
            ],
        ),
    ]

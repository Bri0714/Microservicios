# Generated by Django 4.2 on 2024-11-05 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Conductor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre del Conductor')),
                ('apellido', models.CharField(max_length=50, verbose_name='Apellido del Conductor')),
                ('edad', models.IntegerField(verbose_name='Edad del Conductor')),
                ('telefono', models.CharField(max_length=15, unique=True, verbose_name='Teléfono del Conductor')),
                ('foto', models.ImageField(null=True, upload_to='conductores_fotos/', verbose_name='Foto del Conductor')),
                ('fecha_exp', models.DateField(verbose_name='Fecha de Expedición de Licencia')),
                ('fecha_expiracion', models.DateField(blank=True, null=True, verbose_name='Fecha de Expiración de Licencia')),
                ('licencia_activa', models.BooleanField(default=True, verbose_name='Licencia Activa')),
                ('vehiculo_id', models.IntegerField(unique=True, verbose_name='ID del Vehículo')),
                ('user_id', models.IntegerField()),
            ],
        ),
    ]

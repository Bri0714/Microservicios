# Generated by Django 4.2 on 2024-11-16 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Institucion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institucion_logo', models.ImageField(blank=True, null=True, upload_to='logos/')),
                ('institucion_nombre', models.CharField(max_length=50, verbose_name='Nombre')),
                ('institucion_direccion', models.CharField(max_length=50, verbose_name='Direccion')),
                ('institucion_nit', models.CharField(max_length=20, verbose_name='Nit')),
                ('institucion_contactos', models.EmailField(max_length=254, verbose_name='Correo Electronico')),
                ('institucion_telefono', models.CharField(max_length=50, verbose_name='Telefono')),
                ('user_id', models.IntegerField()),
            ],
            options={
                'unique_together': {('user_id', 'institucion_telefono', 'institucion_contactos')},
            },
        ),
    ]

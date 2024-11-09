# Generated by Django 4.2 on 2024-11-06 20:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Acudiente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acudiente_nombre', models.CharField(max_length=100)),
                ('acudiente_apellido', models.CharField(max_length=200)),
                ('acudiente_parentesco', models.CharField(choices=[('Padre', 'Padre'), ('Madre', 'Madre'), ('Tio', 'Tio'), ('Abuelo', 'Abuelo'), ('Otro', 'Otro')], max_length=50)),
                ('acudiente_telefono', models.CharField(max_length=40)),
                ('user_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Estudiante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('colegio_id', models.IntegerField()),
                ('ruta_id', models.IntegerField()),
                ('estudiante_foto', models.ImageField(blank=True, null=True, upload_to='logos/')),
                ('estudiante_nombre', models.CharField(max_length=100)),
                ('estudiante_apellido', models.CharField(max_length=100)),
                ('estudiante_edad', models.PositiveIntegerField()),
                ('estudiante_curso', models.CharField(max_length=50)),
                ('estudiante_direccion', models.CharField(max_length=255)),
                ('estudiante_fecha_ingreso_ruta', models.DateField()),
                ('estudiante_estado', models.BooleanField(default=True)),
                ('user_id', models.IntegerField()),
                ('acudiente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='estudiantes', to='api.acudiente')),
            ],
        ),
    ]

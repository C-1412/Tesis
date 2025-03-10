# Generated by Django 5.0.2 on 2025-02-05 03:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Nombre')),
            ],
            options={
                'verbose_name': 'Area',
                'verbose_name_plural': 'Area',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Dominio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Nombre')),
            ],
            options={
                'verbose_name': 'Dominio',
                'verbose_name_plural': 'Dominios',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Escala',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Nombre')),
                ('desc', models.CharField(max_length=500, verbose_name='Descripción')),
            ],
            options={
                'verbose_name': 'Escala',
                'verbose_name_plural': 'Escalas',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Indicador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Nombre')),
            ],
            options={
                'verbose_name': 'Indicador',
                'verbose_name_plural': 'Indicadores',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Nombre')),
                ('sec', models.CharField(blank=True, max_length=150, null=True, verbose_name='Sección')),
                ('dom', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='erp.dominio', verbose_name='Dominio')),
            ],
            options={
                'verbose_name': 'Dimensión',
                'verbose_name_plural': 'Dimensiones',
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='dominio',
            name='escalas',
            field=models.ManyToManyField(blank=True, to='erp.escala', verbose_name='Escalas'),
        ),
    ]

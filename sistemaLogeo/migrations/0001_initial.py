# Generated by Django 5.0.6 on 2024-06-21 11:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OBRA',
            fields=[
                ('CodObra', models.AutoField(primary_key=True, serialize=False)),
                ('NomObra', models.CharField(max_length=60)),
                ('NomCon', models.CharField(max_length=60)),
                ('HorMin', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UNIDAD',
            fields=[
                ('CodUni', models.CharField(max_length=60, primary_key=True, serialize=False)),
                ('NomUni', models.CharField(max_length=60)),
                ('ModUni', models.CharField(max_length=60)),
                ('PreHor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('HorUni', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='LABOR',
            fields=[
                ('CodLab', models.AutoField(primary_key=True, serialize=False)),
                ('LabDes', models.CharField(max_length=60)),
                ('CodUsu', models.ForeignKey(db_column='CodUsu', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('CodUni', models.ForeignKey(db_column='CodUni', on_delete=django.db.models.deletion.CASCADE, to='sistemaLogeo.unidad')),
            ],
        ),
        migrations.CreateModel(
            name='TRABAJO',
            fields=[
                ('CodTra', models.AutoField(primary_key=True, serialize=False)),
                ('FecIni', models.DateField()),
                ('FecFin', models.DateField()),
                ('CodLab', models.ForeignKey(db_column='CodLab', on_delete=django.db.models.deletion.CASCADE, to='sistemaLogeo.labor')),
                ('CodObra', models.ForeignKey(db_column='CodObra', on_delete=django.db.models.deletion.CASCADE, to='sistemaLogeo.obra')),
            ],
        ),
        migrations.CreateModel(
            name='REGISTRO',
            fields=[
                ('CodReg', models.AutoField(primary_key=True, serialize=False)),
                ('FecTra', models.DateField()),
                ('Turno', models.CharField(max_length=5)),
                ('EstMaq', models.CharField(max_length=10)),
                ('HorIni', models.DecimalField(decimal_places=2, max_digits=10)),
                ('HorFin', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fecCre', models.DateTimeField(auto_now_add=True)),
                ('CodTra', models.ForeignKey(db_column='CodTra', on_delete=django.db.models.deletion.CASCADE, to='sistemaLogeo.trabajo')),
            ],
        ),
        migrations.AddConstraint(
            model_name='trabajo',
            constraint=models.UniqueConstraint(fields=('CodLab', 'CodObra'), name='unique_CodLab_CodObra'),
        ),
        migrations.AddConstraint(
            model_name='registro',
            constraint=models.UniqueConstraint(fields=('FecTra', 'CodTra'), name='unique_FecTra_CodTra'),
        ),
        migrations.AddConstraint(
            model_name='labor',
            constraint=models.UniqueConstraint(fields=('CodUsu', 'CodUni'), name='unique_codusu_coduni'),
        ),
    ]

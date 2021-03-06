# Generated by Django 2.1.11 on 2019-10-23 12:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('persona', '0001_initial'),
        ('llantas', '0016_auto_20190402_0205'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriaUnidadMedida',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MovimientoGeneral',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_movimiento', models.DateField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_edited', models.DateTimeField(auto_now=True)),
                ('cantidad', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('precio_unitario', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('observacion', models.TextField(blank=True, null=True)),
                ('creador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='creadror_del_movimiento_almacengeneral', to='persona.Profile')),
                ('destino', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='destino_del_movimiento_almacengeneral', to='persona.Profile')),
                ('origen', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='origen_del_movimiento_almacengeneral', to='persona.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=250, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TipoUnidadMedida',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('-1', 'Mas pequeña que la unidad de medida de referencia'), ('0', 'Unidad de Medida de referencia para esta categoria'), ('1', 'Mas grande que la unidad de medida de referencia')], default='0', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='UnidadMedida',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=30, null=True)),
                ('ratio', models.DecimalField(decimal_places=2, default=1, max_digits=8)),
                ('simbolo', models.CharField(blank=True, max_length=10, null=True)),
                ('categoria', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='general.CategoriaUnidadMedida')),
                ('tipo_unidad', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='general.TipoUnidadMedida')),
            ],
        ),
        migrations.CreateModel(
            name='ValeAlmacenGeneral',
            fields=[
                ('vale_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='llantas.Vale')),
            ],
            bases=('llantas.vale',),
        ),
        migrations.AddField(
            model_name='movimientogeneral',
            name='producto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='general.Producto'),
        ),
        migrations.AddField(
            model_name='movimientogeneral',
            name='tipo_movimiento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='llantas.TipoMovimiento'),
        ),
        migrations.AddField(
            model_name='movimientogeneral',
            name='unidad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='general.UnidadMedida'),
        ),
        migrations.AddField(
            model_name='movimientogeneral',
            name='vale',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='vale_almacengeneral_asociado', to='general.ValeAlmacenGeneral'),
        ),
    ]

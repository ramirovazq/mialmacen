# Generated by Django 2.1.7 on 2019-03-21 17:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('llantas', '0011_movimiento_llanta'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdjuntoVale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload', models.FileField(upload_to='uploads/%Y/%m/%d/')),
                ('vale', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='vale_del_adjunto', to='llantas.Vale')),
            ],
        ),
    ]

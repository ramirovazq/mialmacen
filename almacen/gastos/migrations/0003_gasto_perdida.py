# Generated by Django 2.1.11 on 2020-09-19 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gastos', '0002_auto_20200915_0643'),
    ]

    operations = [
        migrations.AddField(
            model_name='gasto',
            name='perdida',
            field=models.BooleanField(default=True),
        ),
    ]

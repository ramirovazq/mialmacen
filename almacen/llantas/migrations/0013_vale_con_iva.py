# Generated by Django 2.1.7 on 2019-03-22 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('llantas', '0012_adjuntovale'),
    ]

    operations = [
        migrations.AddField(
            model_name='vale',
            name='con_iva',
            field=models.BooleanField(default=True),
        ),
    ]
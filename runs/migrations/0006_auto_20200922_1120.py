# Generated by Django 3.1.1 on 2020-09-22 11:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('runs', '0005_auto_20200922_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perceptletrecord',
            name='parent_concept',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='runs.conceptrecord'),
        ),
    ]

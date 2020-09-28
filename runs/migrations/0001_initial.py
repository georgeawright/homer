# Generated by Django 3.1.1 on 2020-09-21 20:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CodeletRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codelet_id', models.CharField(max_length=200, verbose_name='Codelet ID')),
                ('codelet_type', models.CharField(max_length=200, verbose_name='Codelet ID')),
                ('birth_time', models.IntegerField(verbose_name='Birth Time')),
                ('time_run', models.IntegerField(blank=True, null=True, verbose_name='Time Run')),
                ('urgency', models.FloatField(verbose_name='Urgency')),
                ('follow_up', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Follow Up Codelet+', to='runs.codeletrecord', unique=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='runs.codeletrecord', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ConceptRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('concept_id', models.CharField(max_length=200, verbose_name='Concept ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('activation', models.JSONField(verbose_name='Activation')),
            ],
        ),
        migrations.CreateModel(
            name='RunRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(auto_now_add=True, verbose_name='Completion Time')),
            ],
        ),
        migrations.CreateModel(
            name='PerceptletRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('perceptlet_id', models.CharField(max_length=200, verbose_name='Perceptlet ID')),
                ('time_created', models.IntegerField(verbose_name='Time Created')),
                ('value', models.CharField(max_length=200, verbose_name='Value')),
                ('location', models.JSONField(verbose_name='location')),
                ('activation', models.JSONField(verbose_name='Activation')),
                ('unhappiness', models.JSONField(verbose_name='Unhappiness')),
                ('quality', models.FloatField(verbose_name='quality')),
                ('connections', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='runs.perceptletrecord')),
                ('parent_codelet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='runs.codeletrecord')),
                ('parent_concept', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='runs.conceptrecord')),
                ('run_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='runs.runrecord', unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='conceptrecord',
            name='run_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='runs.runrecord', unique=True),
        ),
        migrations.CreateModel(
            name='CoderackRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codelets_run', models.IntegerField(verbose_name='Codelets Run')),
                ('population', models.IntegerField(verbose_name='Population')),
                ('run_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='runs.runrecord', unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='codeletrecord',
            name='perceptlet_types',
            field=models.ManyToManyField(to='runs.ConceptRecord'),
        ),
        migrations.AddField(
            model_name='codeletrecord',
            name='run_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='runs.runrecord', unique=True),
        ),
        migrations.AddField(
            model_name='codeletrecord',
            name='target_perceptlet',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='runs.perceptletrecord'),
        ),
    ]

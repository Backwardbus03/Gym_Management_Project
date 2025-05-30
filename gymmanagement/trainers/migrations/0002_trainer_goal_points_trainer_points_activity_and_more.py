# Generated by Django 5.1.7 on 2025-04-21 11:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainees', '0003_activity_calorielog_weightlog_workouttarget'),
        ('trainers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainer',
            name='goal_points',
            field=models.IntegerField(default=100),
        ),
        migrations.AddField(
            model_name='trainer',
            name='points',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('duration_minutes', models.PositiveIntegerField()),
                ('treadmill_elevation', models.FloatField(blank=True, null=True)),
                ('notes', models.TextField(blank=True)),
                ('calories_burned', models.FloatField(default=0)),
                ('date', models.DateField(auto_now_add=True)),
                ('trainee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainees.trainee')),
            ],
        ),
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('trainee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainees.trainee')),
                ('trainer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainers.trainer')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='WeightLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight_kg', models.FloatField()),
                ('date', models.DateField(auto_now_add=True)),
                ('trainee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trainer_weight_logs', to='trainees.trainee')),
            ],
        ),
    ]

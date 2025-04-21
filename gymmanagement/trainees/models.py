from django.db import models
from django.core.exceptions import ValidationError
from users.models import CustomUser


class Trainee(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.SET_NULL, null=True, related_name='trainee_profile')
    trainer = models.ForeignKey(
        CustomUser,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        limit_choices_to={'role': 'trainer'},
        related_name='assigned_trainees'
    )

    def clean(self):
        if self.user.role.lower() != 'trainee':
            raise ValidationError('Only users with role "trainee" can have a TraineeProfile.')


class Activity(models.Model):
    trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE, related_name='activities')
    name = models.CharField(max_length=100)
    duration_minutes = models.PositiveIntegerField()
    treadmill_elevation = models.FloatField(null=True, blank=True)
    notes = models.TextField(blank=True)
    calories_burned = models.FloatField(default=0)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.duration_minutes} min)"


class CalorieLog(models.Model):
    trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    calories_burned = models.FloatField()
    calories_consumed = models.FloatField()


class WorkoutTarget(models.Model):
    trainee = models.OneToOneField(Trainee, on_delete=models.CASCADE)
    weekly_minutes = models.PositiveIntegerField(default=150)
    target_calories = models.FloatField(default=2000)
    target_weight = models.FloatField(null=True, blank=True)


class WeightLog(models.Model):
    trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE)
    weight_kg = models.FloatField()
    date = models.DateField(auto_now_add=True)
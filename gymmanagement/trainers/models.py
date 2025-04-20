from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
custom_user = get_user_model()

class Trainer(models.Model):
    user = models.OneToOneField(custom_user, on_delete=models.SET_NULL, related_name='trainer_profile', null=True)
    age = models.IntegerField(default=0)
    experience = models.IntegerField(default=0)
    specialisation = models.CharField(max_length=100)
    rate = models.FloatField(default=0)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def check_experience(self):
        if self.experience <= 0:
            raise ValidationError("Experience cannot be 0")
        elif self.experience > self.age:
            raise ValidationError("Experience cannot be over age")


    def time_error(self):
        if self.start_time <= self.end_time:
            raise ValidationError("Start time cannot be after end time")


    def clean(self):
        if self.user.role.lower() != 'trainer':
            raise ValidationError('Only users with role "trainer" can have a TrainerProfile.')
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Trainee(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, related_name='trainee_profile', null=True)
    trainer = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        limit_choices_to={'role': 'trainer'},
        related_name='assigned_trainees'
    )
    goal = models.TextField()

    def clean(self):
        if self.user.role.lower() != 'trainee':
            raise ValidationError('Only users with role "trainee" can have a TraineeProfile.')

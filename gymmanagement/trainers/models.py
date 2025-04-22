from django.db import models
from django.core.exceptions import ValidationError
from users.models import CustomUser
from django.utils.timezone import now

class Trainer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='trainer_profile', null=True)
    age = models.IntegerField(default=0)
    experience = models.IntegerField(default=0)
    specialisation = models.CharField(max_length=100)
    rate = models.FloatField(default=0)
    start_time = models.TimeField()
    end_time = models.TimeField()
    points = models.IntegerField(default=0)
    goal_points = models.IntegerField(default=100)

    def check_experience(self):
        if self.experience <= 0:
            raise ValidationError("Experience cannot be 0")
        elif self.experience > self.age:
            raise ValidationError("Experience cannot be over age")

    def time_error(self):
        if self.start_time <= self.end_time:
            raise ValidationError("Start time cannot be after end time")

    def get_assigned_trainees(self):
        from trainees.models import Trainee
        return Trainee.objects.filter(trainer=self.user)

    def get_todays_activities(self):
        from trainees.models import Activity
        return Activity.objects.filter(date=now().date(), trainee__trainer=self.user)

    def get_todays_weight_logs(self):
        from trainees.models import WeightLog
        return WeightLog.objects.filter(date=now().date(), trainee__trainer=self.user)

    def __str__(self):
        return self.user.username if self.user else "Unassigned Trainer"

class Recommendation(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    trainee = models.ForeignKey('trainees.Trainee', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recommendation from {self.trainer.user.username} to {self.trainee.user.username}"

    class Meta:
        ordering = ['-created_at']

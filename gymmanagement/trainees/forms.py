from django import forms
from .models import Activity, WeightLog

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['name', 'duration_minutes', 'treadmill_elevation', 'notes', 'calories_burned']

class WeightLogForm(forms.ModelForm):
    class Meta:
        model = WeightLog
        fields = ['weight_kg']
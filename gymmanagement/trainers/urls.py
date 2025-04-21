from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.trainer_login, name='trainer_login'),
    path('signup/', views.trainer_signup, name='trainer_signup'),
    path('dashboard/', views.trainer_dashboard, name='trainer_dashboard'),
    path('recommend/<int:trainee_id>/', views.push_recommendation, name='push_recommendation'),
    path('workouts/', views.workout_summary, name='trainer_workouts'),
    path('attendance/', views.view_attendance, name='trainer_attendance'),
]
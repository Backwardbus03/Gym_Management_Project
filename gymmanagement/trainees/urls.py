from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.trainee_login, name='trainee_login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('signup/', views.trainee_signup, name='trainee_signup'),
    path('dashboard/', views.trainee_dashboard, name='trainee_dashboard'),
    path('log-activity/', views.log_activity, name='log_activity'),
    path('log-weight/', views.log_weight, name='log_weight'),
    path('workout-target/', views.view_workout_target, name='view_workout_target'),
    path('workout-target/create/', views.create_workout_target, name='create_workout_target'),
    path('workout-target/update/', views.update_workout_target, name='update_workout_target'),
    path('calorie-log/', views.view_calorie_log, name='view_calorie_log'),
    path('calorie-log/add/', views.log_calories, name='log_calories'),
    path('activities/', views.view_activities, name='view_activities'),
    path('activities/delete/<int:activity_id>/', views.delete_activity, name='delete_activity'),
    path('weight-logs/', views.view_weight_logs, name='view_weight_logs'),
    path('weight-logs/delete/<int:log_id>/', views.delete_weight_log, name='delete_weight_log'),
    path('calorie-log/delete/<int:log_id>/', views.delete_calorie_log, name='delete_calorie_log'),
]
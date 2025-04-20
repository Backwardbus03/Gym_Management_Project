from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.trainee_login, name='trainee_login'),
    path('signup/', views.trainee_signup, name='trainee_signup'),
    path('dashboard/', views.dashboard, name='trainee_dashboard'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.trainer_login, name='trainer_login'),
    path('signup/', views.trainer_signup, name='trainer_signup'),
    path('dashboard/', views.dashboard, name='trainer_dashboard'),
]
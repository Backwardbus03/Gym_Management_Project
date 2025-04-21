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
]
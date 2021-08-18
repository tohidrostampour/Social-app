from django.urls import path
from .views import *

app_name = 'account'
urlpatterns = [
    path('login/',user_login,name='login'),
    path('register/',user_register, name='register'),
    path('logout/',user_logout, name='logout'),
    path('dashboard/<int:user_id>', user_dashboard, name='dashboard')
]
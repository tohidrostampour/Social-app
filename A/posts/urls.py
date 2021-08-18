from django.urls import path
from .views import *


app_name = 'posts'
urlpatterns = [
    path('',all_posts, name='all_posts'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', post_detail, name='post_detail'),
]
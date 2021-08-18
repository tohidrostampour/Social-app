from django.urls import path
from .views import *


app_name = 'posts'
urlpatterns = [
    path('',all_posts, name='all_posts'),
    path('<int:user_id>/<int:year>/<int:month>/<int:day>/<slug:slug>/', post_detail, name='post_detail'),
    path('add_post/<int:user_id>/',add_post,name='add_post')
]
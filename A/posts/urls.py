from django.urls import path
from .views import *


app_name = 'posts'
urlpatterns = [
    path('',all_posts, name='all_posts'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', post_detail, name='post_detail'),
    path('add_post/<int:user_id>/',add_post,name='add_post'),
    path('delete_post/<int:user_id>/<int:post_id>/',delete_post,name='delete_post'),
    path('edit_post/<int:user_id>/<int:post_id>/',edit_post, name='edit_post'),
]
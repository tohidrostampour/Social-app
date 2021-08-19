from django.contrib import admin
from .models import Post,Comment


# admin.site.register(Post)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_filter = ['user']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass

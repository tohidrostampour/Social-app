from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.urls import reverse



class Post(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    body = models.TextField()
    slug = models.SlugField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.body[:30]}'

    def get_absolute_url(self):
        return reverse("posts:post_detail", args=[self.created.year,
            self.created.month,self.created.day,self.slug])
        

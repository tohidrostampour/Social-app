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
        

class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_comment')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='post_comment')
    reply = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='reply_comment')
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.user}-{self.body[:30]}'

    class Meta:
        ordering = ('-created',)
        
from django.shortcuts import get_object_or_404, redirect, render
from .models import Post


def all_posts(request):
    posts = Post.objects.all()
    return render(request,'posts/all_posts.html', {'posts':posts})


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post,created__year=year,created__month=month,
        created__day=day,slug=slug)
    return render(request,'posts/post_detail.html',{'post':post})

from django.shortcuts import get_object_or_404, redirect, render
from .models import Post
from .forms import AddPostForm
from django.utils.text import slugify
from django.contrib import messages




def all_posts(request):
    posts = Post.objects.all()
    return render(request,'posts/all_posts.html', {'posts':posts})


def post_detail(request,user_id,year, month, day, slug):
    post = get_object_or_404(Post,id=user_id,created__year=year,created__month=month,
        created__day=day,slug=slug)
    return render(request,'posts/post_detail.html',{'post':post})


def add_post(request, user_id):
    if request.method == 'POST':
        form = AddPostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.save()
            messages.success(request, "Post Added Successfully!", 'success')
            return redirect('account:dashboard',user_id)
    else:
        form = AddPostForm()
    return render(request, 'posts/add_post.html',{'form':form})
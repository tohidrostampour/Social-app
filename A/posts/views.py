from django.contrib.messages.api import error
from django.shortcuts import get_object_or_404, redirect, render
from .models import Post
from .forms import AddPostForm, EditPostForm
from django.utils.text import slugify
from django.contrib import messages
from django.contrib.auth.decorators import login_required




def all_posts(request):
    posts = Post.objects.all()
    return render(request,'posts/all_posts.html', {'posts':posts})


def post_detail(request,year, month, day, slug):
    post = get_object_or_404(Post,created__year=year,created__month=month,
        created__day=day,slug=slug)
    return render(request,'posts/post_detail.html',{'post':post})

@login_required
def add_post(request, user_id):
    if request.user.id == user_id:
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
    else:
        return redirect(request,'posts:all_posts')


@login_required
def delete_post(request, user_id, post_id):
    if user_id == request.user.id:
        Post.objects.filter(id=post_id).delete()
        messages.success(request,'Your post deleted successfully','success')
        return redirect('account:dashboard',user_id)
    else:
        return redirect('posts:all_posts')


@login_required
def edit_post(request,user_id,post_id):
    if user_id == request.user.id:
        post = get_object_or_404(Post,pk=post_id)
        if request.method == 'POST':
            form = EditPostForm(request.POST,instance=post)
            if form.is_valid():
                edited = form.save(commit=False)
                edited.slug = slugify(form.cleaned_data['body'][:30])
                edited.save()
                messages.success(request,'Your post edited successfully','success')
                return redirect('account:dashboard',user_id)
        else:
            form = EditPostForm(instance=post)
        return render(request,'posts/edit_post.html',{'form':form})
    else:
        return redirect('posts:all_posts')
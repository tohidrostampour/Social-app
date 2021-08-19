from django.contrib.messages.api import error
from django.shortcuts import get_object_or_404, redirect, render
from .models import Post,Comment
from .forms import AddPostForm, EditPostForm, AddCommentForm, AddReplyForm
from django.utils.text import slugify
from django.contrib import messages
from django.contrib.auth.decorators import login_required




def all_posts(request):
    posts = Post.objects.all()
    return render(request,'posts/all_posts.html', {'posts':posts})


def post_detail(request,year, month, day, slug):
    post = get_object_or_404(Post,created__year=year,created__month=month,
        created__day=day,slug=slug)
    comments = Comment.objects.filter(post=post,is_reply=False)
    reply_form = AddReplyForm()
    if request.method == 'POST':
        form = AddCommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user
            new_comment.save()
            messages.success(request,'Your Comment Submitted Successfully','success')
    else:
        form = AddCommentForm()
    return render(request,'posts/post_detail.html',{'post':post,'comments':comments,'form':form,
            'reply':reply_form,
        })

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



@login_required
def add_reply(request,post_id,comment_id):
    post = get_object_or_404(Post,id=post_id)
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        form = AddReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.is_reply = True
            reply.user = request.user
            reply.post = post
            reply.reply = comment
            reply.save()
            messages.success(request,'Reply Submitted Successfully!','success')
    return redirect('posts:post_detail',post.created.year,post.created.month,
            post.created.day, post.slug)
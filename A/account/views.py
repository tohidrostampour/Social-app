from django.shortcuts import redirect, render, get_object_or_404
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from posts.models import Post
from django.contrib.auth.decorators import login_required




def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],password=cd['password'])
            if user is not None:
                login(request,user)
                messages.success(request,'You logged in successfully!','success')
                return redirect('posts:all_posts')
            else:
                messages.error(request,'Wrong username or password!','warning')

    else:
        form = UserLoginForm()
    return render(request,'account/login.html',{'form':form})


def user_register(request):
    if request.method == 'POST':
        next = request.GET.get('next')
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(cd['username'],cd['email'],cd['password'])
            messages.success(request,'You registered successfully','success')
            login(request,user)
            if next:
                return redirect(next)
            return redirect('posts:all_posts')
    else:
        form = UserRegisterationForm()
    return render(request,'account/register.html',{'form':form})

@login_required
def user_logout(request):
    logout(request)
    messages.success(request,'You logged out successfully','success')
    return redirect('posts:all_posts')

@login_required
def user_dashboard(request, user_id):
    user = get_object_or_404(User, id=user_id)
    posts = Post.objects.filter(user=user)
    return render(request,'account/dashboard.html',{'user':user, 'posts':posts})
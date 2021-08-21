from django.shortcuts import redirect, render, get_object_or_404
from requests.api import get
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from posts.models import Post
from django.contrib.auth.decorators import login_required
from random import randint
from kavenegar import *





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
    is_user = False
    if request.user.id == user_id:
        is_user = True
    return render(request,'account/dashboard.html',{'user':user, 'posts':posts,'is_user':is_user})


@login_required
def edit_profile(request, user_id):
    user = get_object_or_404(User,pk=user_id)
    if request.method == 'POST':
        profile_form = EditProfileForm(request.POST, instance=user.profile)
        if profile_form.is_valid():
            cd = profile_form.cleaned_data
            profile_form.save()
            user.email = cd['email']
            user.first_name = cd['first_name']
            user.last_name = cd['last_name']
            user.profile.phone = cd['phone']
            user.save()
            messages.success(request,'Updated Successfully','success')
            return redirect('account:dashboard',user_id)
    else:
        profile_form = EditProfileForm(instance=user.profile,initial={
            'email':user.email,
            'first_name':user.first_name,
            'last_name' : user.last_name,
            'phone':user.profile.phone
        })

    return render(request,'account/edit_profile.html',{'form':profile_form})


def phone_login(request):
    if request.method == 'POST':
        form = PhoneLoginForm(request.POST)
        if form.is_valid():
            phone = f"0{form.cleaned_data['phone']}"
            random_num = randint(1000,9999)
            api = KavenegarAPI('304475437070436E32496134384F36474A3642436D5379395763372F4E6434767278796745376368396D453D')
            params = {
                'sender' : '1000596446',
                'receptor': phone,
                'message' :f'Your Login Code Is: {random_num}' 
                }
            response = api.sms_send(params)
            return redirect('account:verify',phone,random_num)

    else:
        form = PhoneLoginForm()
    return render(request, 'account/phone_login.html',{'form':form})


def verify(request, phone, code):
    if request.method == 'POST':
        form = VerifyCodeForm(request.POST)
        if form.is_valid():
            if code == form.cleaned_data['code']:
                profile = get_object_or_404(Profile, phone=phone)
                user = get_object_or_404(User,profile__id=profile.id)
                login(request,user)
                messages.success(request,'Logged in successfully','success')
                return redirect('posts:all_posts')
            else:
                messages.error('Wrong Code!','warning')
    else:
        form = VerifyCodeForm()
        return render(request,'account/verify.html',{'form':form})
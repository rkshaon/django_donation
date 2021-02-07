from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
import requests
from donation_site.forms import CreateUserForm, CreatePostForm, CreateDonationForm
from donation_site.models import Post, Donation

def index(request):
    posts = Post.objects.all().order_by('-id')
    total_donation = Donation.objects.aggregate(Sum('amount'))
    context = {
        'title': 'Home | Donation Center',
        'post_list': posts,
        'total_donation': total_donation,
    }
    template = loader.get_template('post_list.html')
    return HttpResponse(template.render(context, request))

def about(request):
    total_donation = Donation.objects.aggregate(Sum('amount'))
    context = {'title': 'About | Donation Center', 'total_donation': total_donation,}
    template = loader.get_template('about.html')
    return HttpResponse(template.render(context, request))

@login_required(login_url='login_page')
def my_posts(request):
    posts = Post.objects.filter(author=request.user.id).order_by('-id')
    total_donation = Donation.objects.aggregate(Sum('amount'))
    context = {
        'title': 'Posts | Donation Center',
        'post_list': posts,
        'total_donation': total_donation,
    }
    template = loader.get_template('post_list.html')
    return HttpResponse(template.render(context, request))

def organization(request, pk):
    posts = Post.objects.filter(author=pk).order_by('-id')
    total_donation = Donation.objects.aggregate(Sum('amount'))
    author = User.objects.get(id=pk)
    donate = True
    context = {
        'title': 'Posts | Donation Center',
        'post_list': posts,
        'donate': donate,
        'author': author,
        'total_donation': total_donation,
    }
    template = loader.get_template('post_list.html')
    return HttpResponse(template.render(context, request))

def post(request, pk):
    post = Post.objects.get(id=pk)
    total_donation = Donation.objects.aggregate(Sum('amount'))
    donate = False
    context = {
        'title': 'Post | Donation Center',
        'post': post,
        'donate': donate,
        'total_donation': total_donation,
    }
    template = loader.get_template('post_detail.html')
    return HttpResponse(template.render(context, request))

@login_required(login_url='login_page')
def create_post(request):
    total_donation = Donation.objects.aggregate(Sum('amount'))
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid:
            form.save()
            return redirect('my_posts')
    else:
        pass
    form = CreatePostForm()
    context = {
        'title': 'New Post | Donation Center',
        'form': form,
        'total_donation': total_donation,
    }
    template = loader.get_template('post_form.html')
    return HttpResponse(template.render(context, request))

def registration_page(request):
    total_donation = Donation.objects.aggregate(Sum('amount'))
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid:
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account created for ' + user + '!')
                return redirect('login_page')

    context = {
        'title': 'Registration | Donation Center',
        'form': form,
        'total_donation': total_donation,
    }
    template = loader.get_template('registration.html')
    return HttpResponse(template.render(context, request))

def login_page(request):
    total_donation = Donation.objects.aggregate(Sum('amount'))
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.info(request, "Username OR Password is incorrect!")

        context = {
            'title': 'Login | Donation Center',
            'total_donation': total_donation,
        }
        template = loader.get_template('login.html')
        return HttpResponse(template.render(context, request))

def logout_page(request):
    logout(request)
    return redirect('login_page')

def donation_page(request, pk):
    author = User.objects.get(id=pk)
    total_donation = Donation.objects.aggregate(Sum('amount'))
    form = CreateDonationForm()
    # if request.method == 'POST':
    #     form = CreatePostForm(request.POST, request.FILES)
    #     if form.is_valid:
    #         form.save()
    #         return redirect('my_posts')
    if request.method == 'POST':
        print('Post data: ', request.POST)
        form = CreateDonationForm(request.POST)
        if form.is_valid:
            print('validated')
            form.save()
            return redirect('index')
        else:
            print('validation failed')
    context = {
        'title': 'Donate | Donation Center',
        'author': author,
        'form': form,
        'total_donation': total_donation,
    }
    template = loader.get_template('donate.html')
    return HttpResponse(template.render(context, request))

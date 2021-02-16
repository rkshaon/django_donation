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
    page = 'home'
    context = {
        'title': 'Home | Donation Center',
        'post_list': posts,
        'total_donation': total_donation,
        'page': page,
    }
    template = loader.get_template('post_list.html')
    return HttpResponse(template.render(context, request))

def about(request):
    total_donation = Donation.objects.aggregate(Sum('amount'))
    page = 'about'
    context = {
        'title': 'About | Donation Center',
        'total_donation': total_donation,
        'page': page,
    }
    template = loader.get_template('about.html')
    return HttpResponse(template.render(context, request))

@login_required(login_url='login_page')
def my_posts(request):
    posts = Post.objects.filter(author=request.user.id).order_by('-id')
    total_donation = Donation.objects.aggregate(Sum('amount'))
    page = 'my_post'
    context = {
        'title': 'Posts | Donation Center',
        'post_list': posts,
        'total_donation': total_donation,
        'page': page,
    }
    template = loader.get_template('post_list.html')
    return HttpResponse(template.render(context, request))

def organization(request, pk):
    posts = Post.objects.filter(author=pk).order_by('-id')
    total_donation = Donation.objects.aggregate(Sum('amount'))
    author = User.objects.get(id=pk)
    donate = True
    page = 'organization'
    context = {
        'title': 'Posts | Donation Center',
        'post_list': posts,
        'donate': donate,
        'author': author,
        'total_donation': total_donation,
        'page': page,
    }
    template = loader.get_template('post_list.html')
    return HttpResponse(template.render(context, request))

def post(request, pk):
    post = Post.objects.get(id=pk)
    total_donation = Donation.objects.aggregate(Sum('amount'))
    donate = False
    page = 'post'
    context = {
        'title': 'Post | Donation Center',
        'post': post,
        'donate': donate,
        'total_donation': total_donation,
        'page': page,
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
    page = 'new_post'
    context = {
        'title': 'New Post | Donation Center',
        'form': form,
        'total_donation': total_donation,
        'page': page,
    }
    template = loader.get_template('post_form.html')
    return HttpResponse(template.render(context, request))

def registration_page(request):
    total_donation = Donation.objects.aggregate(Sum('amount'))
    page = 'registration'
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
            else:
                messages.info(request, "Username OR Password is incorrect!")

    context = {
        'title': 'Registration | Donation Center',
        'form': form,
        'total_donation': total_donation,
        'page': page,
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

        page = 'login'
        context = {
            'title': 'Login | Donation Center',
            'total_donation': total_donation,
            'page': page,
        }
        template = loader.get_template('login.html')
        return HttpResponse(template.render(context, request))

def logout_page(request):
    logout(request)
    return redirect('login_page')

@login_required(login_url='login_page')
def donation_page(request, pk):
    author = User.objects.get(id=pk)
    total_donation = Donation.objects.aggregate(Sum('amount'))
    form = CreateDonationForm()
    page = 'new_donation'
    if request.method == 'POST':
        print('Post data: ', request.POST)
        form = CreateDonationForm(request.POST)
        if form.is_valid:
            print('validated')
            form.save()
            return redirect('donation_list')
        else:
            print('validation failed')
    context = {
        'title': 'Donate | Donation Center',
        'author': author,
        'form': form,
        'total_donation': total_donation,
        'page': page,
    }
    template = loader.get_template('donate.html')
    return HttpResponse(template.render(context, request))

def donation_list(request):
    donations = Donation.objects.all().order_by('-id')
    total_donation = Donation.objects.aggregate(Sum('amount'))
    donate = False
    page = 'donation_list'
    context = {
        'title': 'Donation | Donation Center',
        'donations': donations,
        'donate': donate,
        'total_donation': total_donation,
        'page': page,
    }
    template = loader.get_template('donation_list.html')
    return HttpResponse(template.render(context, request))

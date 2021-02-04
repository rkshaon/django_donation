from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import requests
from donation_site.forms import CreateUserForm
from donation_site.models import Post

def index(request):
    posts = Post.objects.all().order_by('-id')
    context = {
        'title': 'Home | Donation Center',
        'post_list': posts,
    }
    template = loader.get_template('post_list.html')
    return HttpResponse(template.render(context, request))

def about(request):
    context = {'title': 'About | Donation Center'}
    template = loader.get_template('about.html')
    return HttpResponse(template.render(context, request))

def my_posts(request):
    posts = Post.objects.filter(author=request.user.id).order_by('-id')
    context = {
        'title': 'Posts | Donation Center',
        'post_list': posts,
    }
    template = loader.get_template('post_list.html')
    return HttpResponse(template.render(context, request))

def organization(request, pk):
    posts = Post.objects.filter(author=pk).order_by('-id')
    donate = True
    context = {
        'title': 'Posts | Donation Center',
        'post_list': posts,
        'donate': donate,
    }
    template = loader.get_template('post_list.html')
    return HttpResponse(template.render(context, request))

def post(request, pk):
    post = Post.objects.get(id=pk)
    donate = False
    context = {
        'title': 'Post | Donation Center',
        'post': post,
        'donate': donate,
    }
    template = loader.get_template('post_detail.html')
    return HttpResponse(template.render(context, request))

def registration_page(request):
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
    }
    template = loader.get_template('registration.html')
    return HttpResponse(template.render(context, request))

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')

    context = {
        'title': 'Login | Donation Center',
    }
    template = loader.get_template('login.html')
    return HttpResponse(template.render(context, request))

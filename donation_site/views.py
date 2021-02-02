from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
import requests
from donation_site.models import Post

def index(request):
    posts = Post.objects.all().order_by('-id')
    context = {
        'title': 'Posts | Donation Center',
        'post_list': posts,
    }
    template = loader.get_template('post_list.html')
    return HttpResponse(template.render(context, request))

def about(request):
    context = {'title': 'Home | Donation Center'}
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
        'title': 'Posts | Donation Center',
        'post': post,
        'donate': donate,
    }
    template = loader.get_template('post_detail.html')
    return HttpResponse(template.render(context, request))

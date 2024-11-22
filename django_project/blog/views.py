from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.contrib.auth import authenticate, login
from .models import Post


def LoginView(request):
    if render.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

def logout_view(request):
    # Logout the user and return a success message
    request.session.flush()
    return redirect('home')  # Replace with your desired URL


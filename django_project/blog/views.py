from django.shortcuts import render, redirect

from .models import Post

def home(request):
    context = {
        'posts': Post.objects.all()

    }
    return render(request, 'blog/home.html', context)


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

def logout_view(request):
    # Logout the user and return a success message
    request.session.flush()
    return redirect('home')  # Replace with your desired URL


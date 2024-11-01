from lib2to3.fixes.fix_input import context

from django.shortcuts import render
#from django.http import HttpResponse


posts = [
    {
        'author': 'CoreyMS',
        'title': 'Blog Post 1',
        'content': 'First Post Content test',
        'date_posted': 'October 31, 2024'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'First Post Content test',
        'date_posted': 'October 31, 2024'
    }

]



def home(request):
    context = {
        'posts': posts

    }
    return render(request, 'blog/home.html', context)


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


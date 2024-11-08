from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render

# Register your models here.
from .models import Post

def register(request):
    form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

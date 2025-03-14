from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from .models import BlogPost, Comment, Announcement, Holiday

# Register your models here.
#from .models import BlogPost

def register(request):
    form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title',)


@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')
    ordering = ('date',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'body', 'post', 'created_on', 'active')  # Use 'user' instead of 'name'
    list_filter = ('active', 'created_on')
    search_fields = ('user__username', 'body')  # Use 'user__username' for searching by the commenter's username
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)

admin.site.register(BlogPost)
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field

 #Create your models here.
class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    content = CKEditor5Field(config_name='default')
    #content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    post = models.ForeignKey('BlogPost', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link the comment to the user
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Holiday(models.Model):
    name = models.CharField(max_length=100)  # Name of the holiday
    date = models.DateField()  # The exact date of the holiday

    def __str__(self):
        return f"{self.name} ({self.date})"


class CalendarEvent(models.Model):
    title = models.CharField(max_length=200)  # Event title
    description = models.TextField(blank=True, null=True)  # Optional description
    date = models.DateField()  # The date of the event
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Admin who created the event

    def __str__(self):
        return f"{self.title} on {self.date}"


#class Post(models.Model):
#    title = models.CharField(max_length=200)
#    content = models.TextField()
#    date_posted = models.DateTimeField(auto_now_add=True)
#    author = models.ForeignKey(User, on_delete=models.CASCADE)

#    def __str__(self):
#        return self.title


 #Create your models here.
#class BlogPost(models.Model):
#  title = models.CharField(max_length=100)
#  content = models.TextField()
#  created_at = models.DateTimeField(default=timezone.now)
#  author = models.ForeignKey(User, on_delete=models.CASCADE)

def __str__(self):
    return self.title

def get_absolute_url(self):
    return reverse('post-detail', kwargs={'pk': self.pk})


#class Post(models.Model):
#    title = models.CharField(max_length=200)
#    content = models.TextField()
#    date_posted = models.DateTimeField(auto_now_add=True)
#    author = models.ForeignKey(User, on_delete=models.CASCADE)

#    def __str__(self):
#        return self.title
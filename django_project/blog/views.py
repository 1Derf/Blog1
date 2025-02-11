from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import BlogPost, Holiday, Comment
from .forms import CommentForm

from django.utils import timezone
import pytz
from calendar import monthrange
import calendar
from datetime import datetime

def LoginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'blog/login.html', {'title': 'Login'})

def home(request):
    context = {
        'posts': BlogPost.objects.all()
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = BlogPost
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 5

class UserPostListView(ListView):
    model = BlogPost
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return BlogPost.objects.filter(author=user).order_by('-created_at')

class PostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/blogpost_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.object
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BlogPost
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BlogPost
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

def logout_view(request):
    request.session.flush()
    return redirect('home')

def latest_posts(request):
    posts = BlogPost.objects.order_by('-created_at')[:5]
    return render(request, 'blog/latest-post.html', {'posts': posts})

from calendar import month_name

def calendar_view(request):
    from calendar import monthrange
    import pytz
    from django.utils import timezone

    # Get the current date
    arizona_tz = pytz.timezone('America/Phoenix')
    now = timezone.now().astimezone(arizona_tz)

    # Get the year and month from the query parameters (default: current month)
    year = int(request.GET.get('year', now.year))  # Default to the current year
    month = int(request.GET.get('month', now.month))  # Default to the current month

    # Handle month/year boundaries (e.g., going from December to January)
    if month < 1:
        month = 12
        year -= 1
    elif month > 12:
        month = 1
        year += 1

    # Get the full name of the month (e.g., "September")
    month_name_full = month_name[month]

    # Get the first day of the month and number of days in the month
    first_day_of_month, days_in_month = monthrange(year, month)

    # Adjust first day to align with Sunday as the start of the week
    first_day_of_month = (first_day_of_month + 1) % 7

    # Generate a list of days and whether each day starts a new row
    days = []
    for i in range(1, days_in_month + 1):
        day_position = first_day_of_month + (i - 1)
        row_break = (day_position % 7 == 6)  # Break after Saturday
        days.append((i, row_break))

    # Initialize posts_by_date as an empty dictionary
    posts_by_date = {}

    # Get posts for the specified month and year
    posts = BlogPost.objects.filter(created_at__year=year, created_at__month=month)

    for post in posts:
        date = post.created_at.day
        if date not in posts_by_date:
            posts_by_date[date] = []
        posts_by_date[date].append(post)

    # Get holidays for the specified month and year
    holidays = Holiday.objects.filter(date__year=year, date__month=month)

    # Group holidays by date
    holidays_by_date = {}
    for holiday in holidays:
        if holiday.date.day not in holidays_by_date:
            holidays_by_date[holiday.date.day] = []
        holidays_by_date[holiday.date.day].append(holiday.name)

    # Calculate how many empty cells are needed in the last row
    total_cells = 7 * ((days_in_month + first_day_of_month + 6) // 7)
    empty_cells_last_row = total_cells - (days_in_month + first_day_of_month)

    empty_cells_last_row_list = range(empty_cells_last_row) if empty_cells_last_row > 0 else []

    # Add navigation links for previous/next months
    previous_month = month - 1
    previous_year = year
    if previous_month < 1:  # If it's January, move to December of the previous year
        previous_month = 12
        previous_year -= 1

    next_month = month + 1
    next_year = year
    if next_month > 12:  # If it's December, move to January of the next year
        next_month = 1
        next_year += 1

    context = {
        'days': days,
        'posts_by_date': posts_by_date,
        'holidays_by_date': holidays_by_date,
        'month': month,
        'month_name': month_name_full,  # Pass the full month name to the template
        'year': year,
        'first_day_of_month': first_day_of_month,
        'empty_cells': range(first_day_of_month),
        'empty_cells_last_row': empty_cells_last_row_list,

        # Add navigation data to the context
        'previous_month': previous_month,
        'previous_year': previous_year,
        'next_month': next_month,
        'next_year': next_year,
    }
    return render(request, 'blog/calendar.html', context)

@login_required
def blog_post_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    comments = post.comments.filter(active=True)  # Get all active comments for the post

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)  # Don't save to the database yet
            comment.post = post  # Associate the comment with the current post
            comment.user = request.user  # Associate the comment with the logged-in user
            comment.save()  # Save the comment to the database
            return redirect('post-detail', pk=post.pk)  # Redirect to the same post page
    else:
        form = CommentForm()

    context = {
        'object': post,
        'comments': comments,
        'form': form,
    }
    return render(request, 'blog/blogpost_detail.html', context)

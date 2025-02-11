from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    calendar_view,
    latest_posts,
    blog_post_detail,
)

from . import views
#from .views import views as auth_views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    # Remove PostDetailView
    # path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/', blog_post_detail, name='post-detail'),  # Use the function-based view
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    path('login/', views.LoginView, name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('latest-post/', views.latest_posts, name='latest_posts'),
    path('calendar/', calendar_view, name='calendar'),
]






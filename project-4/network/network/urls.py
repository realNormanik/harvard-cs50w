from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("tweet", views.tweet, name="tweet"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("all-posts", views.allPosts, name="allPosts"),
    path("following", views.following, name="following"),

    # API routes
    path("follow/<int:user_id>", views.follow, name="follow"),
    path("edit/<int:post_id>", views.edit, name="edit"),
    path("delete/<int:post_id>/", views.delete_post, name="delete_post"),
    path("like/<int:post_id>", views.like, name="like")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
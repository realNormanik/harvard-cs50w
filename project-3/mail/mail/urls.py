from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),    # Default route
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # API Routes
    path("emails", views.compose, name="compose"),
    path("emails/<int:email_id>", views.email, name="email"),
    path("emails/<str:mailbox>", views.mailbox, name="mailbox"),    # GET request where mailbox is inbox, sent, or archive. Returns list of emails.

    path("upload-image", views.upload_image, name="upload_image")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
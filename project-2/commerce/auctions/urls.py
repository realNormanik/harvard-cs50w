from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    # Main page
    path("", views.index, name="index"),
    
    # Authentication paths
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    
    # Auction creation and management
    path("create", views.create, name="create"),
    path("insert", views.insert, name="insert"),
    
    # Auction listing details
    path("listing/<int:id>", views.listing, name="listing"),
    
    # Watchlist functionality
    path("watchlist", views.watchlist, name="watchlist"),
    path("watch/<int:id>", views.watch, name="watch"),
    path("unwatch/<int:id>", views.unwatch, name="unwatch"),
    
    # Categories and filtering
    path("categories", views.categories, name="categories"),
    path("filter", views.filter, name="filter"),
    
    # Bid management
    path("update-bid/<int:id>/", views.update_bid, name="update_bid"),
    path("close-bid/<int:id>/", views.close_bid, name="close_bid"),
    
    # Comments
    path("comments/<int:id>", views.add_comment, name="add_comment")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
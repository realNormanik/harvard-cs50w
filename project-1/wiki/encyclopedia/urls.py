from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
# Import the "path" function from Django to define URL patterns and the "views" module from the current directory

app_name = "wiki"
# Define the application namespace as "wiki" for reverse URL resolution

urlpatterns = [
    # Define URL patterns for the "wiki" app

    path("", views.index, name="index"),
    # URL for the homepage, associated with the "index" view and named "index"

    path("new/", views.new, name="new"),
    # URL for the page to create a new entry, associated with the "new" view and named "new"

    path("random_page/", views.random_page, name="random_page"),
    # URL for viewing a random page, associated with the "random_page" view and named "random_page"

    path("search/", views.search, name="search"),
    # URL for the search page, associated with the "search" view and named "search"

    path("wiki/<str:entry>/", views.page, name="page"),
    # URL pattern that dynamically matches any entry name and links it to the "page" view with the entry name as a string parameter

    path("<str:entry>/edit/", views.edit, name="edit"),
    # URL pattern for editing an entry, dynamically matched by the entry name and associated with the "edit" view
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
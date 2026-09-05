from django.urls import path
from . import views


urlpatterns = [
    # Authentication routes
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # Main application views
    path("", views.pipeline, name="pipeline"),
    path("clients", views.client_list, name="client_list"),
    path("clients/<int:client_id>", views.client_detail, name="client_detail"),
    path("clients/new", views.client_create, name="client_create"),
    path("tasks", views.task_list, name="task_list"),
    path("tasks/<int:task_id>/toggle", views.task_toggle, name="task_toggle"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("stages", views.stage_settings, name="stage_settings"),

    # API endpoints used by fetch requests
    # These endpoints handle drag-and-drop, modal editing, and searching
    path("api/deals/create", views.api_deal_create, name="api_deal_create"),
    path("api/deals/<int:deal_id>", views.api_deal_detail, name="api_deal_detail"),
    path("api/deals/<int:deal_id>/move", views.api_deal_move, name="api_deal_move"),
    path(
        "api/deals/<int:deal_id>/toggle-complete",
        views.api_deal_toggle_complete,
        name="api_deal_toggle_complete",
    ),
    path("api/deals/<int:deal_id>/delete", views.api_deal_delete, name="api_deal_delete"),
    path("api/clients/search", views.api_client_search, name="api_client_search"),
    path("api/stages/reorder", views.api_stage_reorder, name="api_stage_reorder"),
]

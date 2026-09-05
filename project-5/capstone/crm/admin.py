from django.contrib import admin
from .models import Client, PipelineStage, Deal, Activity, Task


# Register the Client model in the Django admin panel
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    # Define the fields displayed in the client list
    list_display = ("first_name", "last_name", "company", "email", "owner", "created_at")

    # Define the fields that can be searched in the admin panel
    search_fields = ("first_name", "last_name", "company", "email")


# Register the PipelineStage model in the Django admin panel
@admin.register(PipelineStage)
class PipelineStageAdmin(admin.ModelAdmin):
    # Define the fields displayed in the pipeline stage list
    list_display = ("name", "order", "owner")

    # Sort pipeline stages by their order value
    ordering = ("order",)


# Register the Deal model in the Django admin panel
@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    # Define the fields displayed in the deal list
    list_display = ("title", "client", "stage", "priority", "value", "due_date", "is_closed")

    # Add filters for stage, priority, and closed status
    list_filter = ("stage", "priority", "is_closed")

    # Define the fields that can be searched in the admin panel
    search_fields = ("title", "client__first_name", "client__last_name")


# Register the Activity model in the Django admin panel
@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    # Define the fields displayed in the activity list
    list_display = ("activity_type", "client", "deal", "created_at")

    # Add a filter for the activity type
    list_filter = ("activity_type",)


# Register the Task model in the Django admin panel
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    # Define the fields displayed in the task list
    list_display = ("title", "client", "deal", "due_date", "is_done")

    # Add a filter for completed and incomplete tasks
    list_filter = ("is_done",)

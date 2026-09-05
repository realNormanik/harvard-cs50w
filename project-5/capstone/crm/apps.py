from django.apps import AppConfig


# Define the configuration for the CRM application
class CrmConfig(AppConfig):

    # Use BigAutoField as the default primary key type for models
    default_auto_field = "django.db.models.BigAutoField"

    # Set the name of the Django application
    name = "crm"

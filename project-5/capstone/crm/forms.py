from django import forms
from .models import Client, Deal, Task, PipelineStage, Activity


# Add Bootstrap CSS classes to form widgets automatically
# This avoids having to define the classes manually for every field
class BootstrapFormMixin:

    # Initialize the form and apply Bootstrap classes to all fields
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Remove the default colon displayed after form labels
        self.label_suffix = ""

        # Iterate through all fields defined in the form
        for field_name, field in self.fields.items():
            widget = field.widget

            # Get any CSS classes already assigned to the widget
            existing_class = widget.attrs.get("class", "")

            # Use the appropriate Bootstrap class based on the widget type
            if isinstance(widget, forms.CheckboxInput):
                css_class = "form-check-input"
            elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
                css_class = "form-select"
            else:
                css_class = "form-control"

            # Add the Bootstrap class while preserving existing classes
            widget.attrs["class"] = f"{existing_class} {css_class}".strip()

            # Use the field name as a fallback if no label is defined
            field.label = field.label or field_name.replace("_", " ").capitalize()


# Form used to create and edit clients
class ClientForm(BootstrapFormMixin, forms.ModelForm):

    class Meta:
        # Specify the model used by this form
        model = Client

        # Define the fields displayed in the form
        fields = ["first_name", "last_name", "company", "email", "phone", "notes"]

        # Customize specific form widgets
        widgets = {
            # Display the notes field as a multi-line text area
            "notes": forms.Textarea(attrs={"rows": 3}),
        }


# Form used to create and edit deals
class DealForm(BootstrapFormMixin, forms.ModelForm):

    class Meta:
        # Specify the model used by this form
        model = Deal

        # Define the fields displayed in the form
        fields = [
            "title",
            "description",
            "client",
            "stage",
            "value",
            "priority",
            "due_date",
        ]

        # Customize specific form widgets
        widgets = {
            # Display the description field as a multi-line text area
            "description": forms.Textarea(attrs={"rows": 3}),

            # Use a date picker for the due date field
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }

    # Initialize the form with an optional owner
    def __init__(self, *args, owner=None, **kwargs):
        super().__init__(*args, **kwargs)

        # Restrict clients and pipeline stages to those belonging to the current user
        if owner is not None:
            self.fields["client"].queryset = Client.objects.filter(owner=owner)
            self.fields["stage"].queryset = PipelineStage.objects.filter(owner=owner)


# Form used to create and edit tasks
class TaskForm(BootstrapFormMixin, forms.ModelForm):

    class Meta:
        # Specify the model used by this form
        model = Task

        # Define the fields displayed in the form
        fields = ["title", "client", "deal", "due_date"]

        # Customize the due date widget
        widgets = {
            # Use a date picker for the due date field
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }

    # Initialize the form with an optional owner
    def __init__(self, *args, owner=None, **kwargs):
        super().__init__(*args, **kwargs)

        # Restrict clients and deals to those belonging to the current user
        if owner is not None:
            self.fields["client"].queryset = Client.objects.filter(owner=owner)
            self.fields["deal"].queryset = Deal.objects.filter(owner=owner)


# Form used to create and edit pipeline stages
class PipelineStageForm(BootstrapFormMixin, forms.ModelForm):

    class Meta:
        # Specify the model used by this form
        model = PipelineStage

        # Define the fields displayed in the form
        fields = ["name", "order"]


# Form used to create and edit activities
class ActivityForm(BootstrapFormMixin, forms.ModelForm):

    class Meta:
        # Specify the model used by this form
        model = Activity

        # Define the fields displayed in the form
        fields = ["client", "deal", "activity_type", "content"]

        # Customize the content widget
        widgets = {
            # Display the content field as a multi-line text area
            "content": forms.Textarea(attrs={"rows": 3}),
        }

    # Initialize the form with an optional owner
    def __init__(self, *args, owner=None, **kwargs):
        super().__init__(*args, **kwargs)

        # Restrict clients and deals to those belonging to the current user
        if owner is not None:
            self.fields["client"].queryset = Client.objects.filter(owner=owner)
            self.fields["deal"].queryset = Deal.objects.filter(owner=owner)

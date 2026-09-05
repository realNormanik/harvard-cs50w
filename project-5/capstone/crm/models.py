from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Represents a stage in the sales pipeline
class PipelineStage(models.Model):
    """Represents a stage in the sales pipeline."""

    # Name of the pipeline stage
    name = models.CharField(max_length=100)

    # Position of the stage in the pipeline
    order = models.PositiveIntegerField(default=0)

    # User who owns this pipeline stage
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="stages"
    )

    # Indicates whether this is a final pipeline stage
    is_final = models.BooleanField(default=False)

    class Meta:
        # Sort pipeline stages by their order value
        ordering = ["order"]

    def __str__(self):
        # Return the stage name when the object is converted to a string
        return self.name


# Represents a business client or contact
class Client(models.Model):
    """Represents a business client or contact."""

    # User who owns this client
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="clients"
    )

    # Client's first name
    first_name = models.CharField(max_length=100)

    # Client's last name
    last_name = models.CharField(max_length=100, blank=True)

    # Client's company name
    company = models.CharField(max_length=150, blank=True)

    # Client's email address
    email = models.EmailField(blank=True)

    # Client's phone number
    phone = models.CharField(max_length=30, blank=True)

    # Additional notes about the client
    notes = models.TextField(blank=True)

    # Automatically store the date and time when the client is created
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Build the client's full name and remove unnecessary whitespace
        full_name = f"{self.first_name} {self.last_name}".strip()

        # Include the company name if one is available
        return f"{full_name} ({self.company})" if self.company else full_name


# Represents a specific deal in the sales pipeline
class Deal(models.Model):
    """Represents a specific deal associated with a client."""

    # Available priority levels for deals
    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    # User who owns this deal
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="deals"
    )

    # Title of the deal
    title = models.CharField(max_length=200)

    # Optional description of the deal
    description = models.TextField(blank=True)

    # Client associated with the deal
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="deals"
    )

    # Pipeline stage associated with the deal
    stage = models.ForeignKey(
        PipelineStage,
        on_delete=models.CASCADE,
        related_name="deals"
    )

    # Monetary value of the deal
    value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    # Priority level of the deal
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default="medium"
    )

    # Optional deadline for the deal
    due_date = models.DateField(null=True, blank=True)

    # Position of the deal card within its pipeline column
    order = models.PositiveIntegerField(default=0)

    # Automatically store the date and time when the deal is created
    created_at = models.DateTimeField(auto_now_add=True)

    # Automatically update the date and time whenever the deal is modified
    updated_at = models.DateTimeField(auto_now=True)

    # Indicates whether the deal has been closed
    is_closed = models.BooleanField(default=False)

    class Meta:
        # Sort deals by their order value
        ordering = ["order"]

    def __str__(self):
        # Return the deal title and associated client
        return f"{self.title} — {self.client}"

    def is_overdue(self):
        # Return True if the deal has a past due date and is not closed
        return bool(
            self.due_date
            and self.due_date < timezone.now().date()
            and not self.is_closed
        )


# Represents a record of an interaction with a client
class Activity(models.Model):
    """Represents a history of interactions with a client."""

    # Available types of client activities
    TYPE_CHOICES = [
        ("call", "Call"),
        ("email", "E-mail"),
        ("meeting", "Meet"),
        ("note", "Note"),
    ]

    # User who owns this activity
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="activities"
    )

    # Client associated with the activity
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="activities"
    )

    # Optional deal associated with the activity
    # The relationship is cleared if the deal is deleted
    deal = models.ForeignKey(
        Deal,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="activities"
    )

    # Type of the activity
    activity_type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES
    )

    # Content or description of the activity
    content = models.TextField()

    # Automatically store the date and time when the activity is created
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Display the newest activities first
        ordering = ["-created_at"]

    def __str__(self):
        # Return the activity type and associated client
        return f"{self.get_activity_type_display()} — {self.client}"


# Represents an independent task or reminder
class Task(models.Model):
    """Represents an independent task or reminder."""

    # User who owns this task
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tasks"
    )

    # Optional client associated with the task
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="tasks"
    )

    # Optional deal associated with the task
    deal = models.ForeignKey(
        Deal,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="tasks"
    )

    # Title of the task
    title = models.CharField(max_length=200)

    # Optional deadline for the task
    due_date = models.DateField(null=True, blank=True)

    # Indicates whether the task has been completed
    is_done = models.BooleanField(default=False)

    # Automatically store the date and time when the task is created
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Sort tasks by due date and then by creation date
        ordering = ["due_date", "-created_at"]

    def __str__(self):
        # Return the task title when the object is converted to a string
        return self.title

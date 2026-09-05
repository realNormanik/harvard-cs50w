import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Sum, Count, Q
from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .models import Client, Deal, PipelineStage, Activity, Task
from .forms import ClientForm, DealForm, TaskForm, PipelineStageForm, ActivityForm


# ---------------------------------------------------------------------------
# AUTHENTICATION
# ---------------------------------------------------------------------------

# Handle user login
def login_view(request):
    if request.method == "POST":
        # Get the username and password submitted by the user
        username = request.POST["username"]
        password = request.POST["password"]

        # Authenticate the user using the provided credentials
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log the authenticated user into the application
            login(request, user)

            # Redirect the user to the main pipeline page
            return redirect("pipeline")

        # Display an error message when authentication fails
        return render(
            request,
            "crm/login.html",
            {"message": "Invalid username or password."}
        )

    # Display the login page for GET requests
    return render(request, "crm/login.html")


# Handle user logout
def logout_view(request):
    # Log the current user out
    logout(request)

    # Redirect the user to the login page
    return redirect("login")


# Handle new user registration
def register(request):
    if request.method == "POST":
        # Get registration data submitted by the user
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        # Check whether both entered passwords match
        if password != confirmation:
            return render(
                request,
                "crm/register.html",
                {"message": "The passwords are not identical."}
            )

        try:
            # Create a new Django user
            user = User.objects.create_user(username, email, password)
            user.save()

        except IntegrityError:
            # Display an error if the username is already in use
            return render(
                request,
                "crm/register.html",
                {"message": "That username is already taken."}
            )

        # Create the default pipeline stages for the new user
        default_stages = [
            "New lead",
            "Contact",
            "Offer sent",
            "Negotiations",
            "Completed"
        ]

        for i, stage_name in enumerate(default_stages):
            PipelineStage.objects.create(
                name=stage_name,
                order=i,
                owner=user
            )

        # Log the newly registered user in automatically
        login(request, user)

        # Redirect the user to the main pipeline page
        return redirect("pipeline")

    # Display the registration page for GET requests
    return render(request, "crm/register.html")


# ---------------------------------------------------------------------------
# PIPELINE
# Main sales pipeline view with drag-and-drop functionality
# ---------------------------------------------------------------------------

# Require the user to be authenticated
@login_required
def pipeline(request):
    # Get all pipeline stages belonging to the current user
    # and prefetch their related deals
    stages = (
        PipelineStage.objects
        .filter(owner=request.user)
        .prefetch_related("deals")
    )

    # Get all clients belonging to the current user
    clients = Client.objects.filter(owner=request.user)

    if request.method == "POST":
        # Create the deal form using submitted data
        # and restrict related objects to the current user
        form = DealForm(request.POST, owner=request.user)

        if form.is_valid():
            # Create the deal without saving the owner yet
            deal = form.save(commit=False)

            # Assign the current user as the deal owner
            deal.owner = request.user

            # Save the deal to the database
            deal.save()

            # Save many-to-many relationships such as tags
            form.save_m2m()

            # Redirect back to the pipeline after successful creation
            return redirect("pipeline")

    else:
        # Create an empty deal form for GET requests
        form = DealForm(owner=request.user)

    # Render the pipeline page with its stages, clients, and form
    return render(
        request,
        "crm/pipeline.html",
        {
            "stages": stages,
            "clients": clients,
            "form": form,
        }
    )


# Handle moving a deal between pipeline stages using drag-and-drop
@login_required
@require_POST
def api_deal_move(request, deal_id):
    """Handle a deal move request sent by JavaScript after drag-and-drop."""

    # Get the deal belonging to the current user
    deal = get_object_or_404(
        Deal,
        id=deal_id,
        owner=request.user
    )

    # Parse the JSON data sent by the client
    data = json.loads(request.body)

    # Get the target stage ID and new position
    new_stage_id = data.get("stage_id")
    new_order = data.get("order")

    # Make sure the target stage also belongs to the current user
    stage = get_object_or_404(
        PipelineStage,
        id=new_stage_id,
        owner=request.user
    )

    # Assign the deal to the new pipeline stage
    deal.stage = stage

    # Update the deal position if one was provided
    if new_order is not None:
        deal.order = new_order

    # Save the updated deal
    deal.save()

    # Return a successful JSON response
    return JsonResponse({
        "success": True,
        "deal_id": deal.id,
        "stage_id": stage.id
    })


# Create a new deal through an API request
@login_required
@require_POST
def api_deal_create(request):
    # Parse the JSON data sent by the client
    data = json.loads(request.body)

    # Validate the submitted data using the deal form
    form = DealForm(data, owner=request.user)

    if form.is_valid():
        # Create the deal without saving the owner yet
        deal = form.save(commit=False)

        # Assign the current user as the deal owner
        deal.owner = request.user

        # Save the deal
        deal.save()

        # Save many-to-many relationships such as tags
        form.save_m2m()

        # Return the newly created deal ID
        return JsonResponse({
            "success": True,
            "deal_id": deal.id
        })

    # Return validation errors when the form is invalid
    return JsonResponse(
        {"success": False, "errors": form.errors},
        status=400
    )


# Retrieve or update a specific deal through the API
@login_required
def api_deal_detail(request, deal_id):
    # Get the deal belonging to the current user
    deal = get_object_or_404(
        Deal,
        id=deal_id,
        owner=request.user
    )

    if request.method == "GET":
        # Return the deal information as JSON
        return JsonResponse({
            "id": deal.id,
            "title": deal.title,
            "description": deal.description,
            "client": deal.client.id,
            "stage": deal.stage.id,
            "value": str(deal.value),
            "priority": deal.priority,
            "due_date": (
                deal.due_date.isoformat()
                if deal.due_date
                else None
            ),
            "is_overdue": deal.is_overdue(),
            "is_closed": deal.is_closed,
        })

    if request.method in ("PUT", "PATCH"):
        # Parse the submitted JSON data
        data = json.loads(request.body)

        # Update the fields included in the request
        for field in ["title", "description", "value", "priority"]:
            if field in data:
                setattr(deal, field, data[field])

        # Update the due date separately because it can be empty
        if "due_date" in data:
            deal.due_date = data["due_date"] or None

        # Save the updated deal
        deal.save()

        # Return a successful response
        return JsonResponse({"success": True})

    # Reject HTTP methods that are not supported by this endpoint
    return HttpResponseNotAllowed(["GET", "PUT", "PATCH"])


# Toggle the closed status of a deal
@login_required
@require_POST
def api_deal_toggle_complete(request, deal_id):
    """Toggle the completion status of a deal."""

    # Get the deal belonging to the current user
    deal = get_object_or_404(
        Deal,
        id=deal_id,
        owner=request.user
    )

    # Toggle the current closed status
    deal.is_closed = not deal.is_closed

    # Save the updated status
    deal.save()

    # Return the new status as JSON
    return JsonResponse({
        "success": True,
        "deal_id": deal.id,
        "is_closed": deal.is_closed
    })


# Delete a deal through the API
@login_required
@require_POST
def api_deal_delete(request, deal_id):
    # Get the deal belonging to the current user
    deal = get_object_or_404(
        Deal,
        id=deal_id,
        owner=request.user
    )

    # Delete the deal from the database
    deal.delete()

    # Return a successful response
    return JsonResponse({"success": True})


# ---------------------------------------------------------------------------
# CLIENTS
# ---------------------------------------------------------------------------

# Display the list of clients and handle client creation
@login_required
def client_list(request):
    if request.method == "POST":
        # Create the client form using submitted data
        form = ClientForm(request.POST)

        if form.is_valid():
            # Create the client without saving the owner yet
            client = form.save(commit=False)

            # Assign the current user as the client owner
            client.owner = request.user

            # Save the client
            client.save()

            # Redirect to the client list
            return redirect("client_list")

    else:
        # Create an empty client form
        form = ClientForm()

    # Get the search query from the URL
    query = request.GET.get("q", "")

    # Start with clients belonging to the current user
    clients = Client.objects.filter(owner=request.user)

    if query:
        # Filter clients by first name, last name, company, or email
        clients = clients.filter(
            Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(company__icontains=query)
            | Q(email__icontains=query)
        )

    # Render the client list page
    return render(
        request,
        "crm/client_list.html",
        {
            "clients": clients,
            "query": query,
            "form": form
        }
    )


# Create a new client
@login_required
def client_create(request):
    if request.method == "POST":
        # Create the client form using submitted data
        form = ClientForm(request.POST)

        if form.is_valid():
            # Create the client without saving the owner yet
            client = form.save(commit=False)

            # Assign the current user as the client owner
            client.owner = request.user

            # Save the client
            client.save()

            # Redirect to the newly created client's detail page
            return redirect(
                "client_detail",
                client_id=client.id
            )

    else:
        # Create an empty client form
        form = ClientForm()

    # Render the client creation form
    return render(
        request,
        "crm/client_form.html",
        {"form": form}
    )


# Display details, activities, and deals for a specific client
@login_required
def client_detail(request, client_id):
    # Get the client belonging to the current user
    client = get_object_or_404(
        Client,
        id=client_id,
        owner=request.user
    )

    # Get all activities and deals associated with the client
    activities = client.activities.all()
    deals = client.deals.all()

    if request.method == "POST":
        # Create an activity form using submitted data
        form = ActivityForm(
            request.POST,
            owner=request.user
        )

        if form.is_valid():
            # Create the activity without saving the owner and client yet
            activity = form.save(commit=False)

            # Assign the current user as the activity owner
            activity.owner = request.user

            # Associate the activity with the current client
            activity.client = client

            # Save the activity
            activity.save()

            # Redirect back to the client's detail page
            return redirect(
                "client_detail",
                client_id=client.id
            )

    else:
        # Create an empty activity form with the current client selected
        form = ActivityForm(
            owner=request.user,
            initial={"client": client}
        )

    # Render the client detail page
    return render(
        request,
        "crm/client_detail.html",
        {
            "client": client,
            "activities": activities,
            "deals": deals,
            "form": form,
        }
    )


# Search for clients through the API
@login_required
def api_client_search(request):
    # Get the search query from the request
    query = request.GET.get("q", "")

    # Start with clients belonging to the current user
    clients = Client.objects.filter(owner=request.user)

    if query:
        # Filter clients by first name, last name, or company
        clients = clients.filter(
            Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(company__icontains=query)
        )

    # Return up to 10 matching clients as JSON
    results = [
        {"id": c.id, "name": str(c)}
        for c in clients[:10]
    ]

    return JsonResponse({"results": results})


# ---------------------------------------------------------------------------
# TASKS
# ---------------------------------------------------------------------------

# Display the task list and handle task creation
@login_required
def task_list(request):
    # Get all tasks belonging to the current user
    tasks = Task.objects.filter(owner=request.user)

    if request.method == "POST":
        # Create the task form using submitted data
        form = TaskForm(
            request.POST,
            owner=request.user
        )

        if form.is_valid():
            # Create the task without saving the owner yet
            task = form.save(commit=False)

            # Assign the current user as the task owner
            task.owner = request.user

            # Save the task
            task.save()

            # Redirect back to the task list
            return redirect("task_list")

    else:
        # Create an empty task form
        form = TaskForm(owner=request.user)

    # Render the task list page
    return render(
        request,
        "crm/task_list.html",
        {
            "tasks": tasks,
            "form": form
        }
    )


# Toggle the completion status of a task
@login_required
@require_POST
def task_toggle(request, task_id):
    # Get the task belonging to the current user
    task = get_object_or_404(
        Task,
        id=task_id,
        owner=request.user
    )

    # Toggle the task completion status
    task.is_done = not task.is_done

    # Save the updated task
    task.save()

    # Return the new completion status as JSON
    return JsonResponse({
        "success": True,
        "is_done": task.is_done
    })


# ---------------------------------------------------------------------------
# PIPELINE STAGES
# ---------------------------------------------------------------------------

# Display and manage the user's pipeline stages
@login_required
def stage_settings(request):
    # Get all pipeline stages belonging to the current user
    stages = PipelineStage.objects.filter(owner=request.user)

    if request.method == "POST":
        # Create the pipeline stage form using submitted data
        form = PipelineStageForm(request.POST)

        if form.is_valid():
            # Create the stage without saving the owner yet
            stage = form.save(commit=False)

            # Assign the current user as the stage owner
            stage.owner = request.user

            # Save the new stage
            stage.save()

            # Redirect back to the stage settings page
            return redirect("stage_settings")

    else:
        # Create an empty pipeline stage form
        form = PipelineStageForm()

    # Render the stage settings page
    return render(
        request,
        "crm/stage_settings.html",
        {
            "stages": stages,
            "form": form
        }
    )


# Save a new pipeline stage order after drag-and-drop
@login_required
@require_POST
def api_stage_reorder(request):
    """Save the new pipeline stage order after drag-and-drop."""

    # Parse the JSON data sent by the client
    data = json.loads(request.body)

    # Get the ordered list of stage IDs
    stage_ids = data.get("order", [])

    # Get only stages belonging to the current user
    # and create a dictionary for quick lookup by ID
    stages = {
        stage.id: stage
        for stage in PipelineStage.objects.filter(
            owner=request.user,
            id__in=stage_ids
        )
    }

    # Update the order value for every stage
    for index, stage_id in enumerate(stage_ids):
        stage = stages.get(int(stage_id))

        if stage:
            # Assign the new position to the stage
            stage.order = index

            # Update only the order field in the database
            stage.save(update_fields=["order"])

    # Return a successful JSON response
    return JsonResponse({"success": True})


# ---------------------------------------------------------------------------
# DASHBOARD / STATISTICS
# ---------------------------------------------------------------------------

# Display sales pipeline statistics
@login_required
def dashboard(request):
    # Get all deals belonging to the current user
    deals = Deal.objects.filter(owner=request.user)

    # Calculate statistics for each pipeline stage
    stage_stats = list(
        PipelineStage.objects
        .filter(owner=request.user)
        .annotate(
            # Count the number of deals in each stage
            deal_count=Count("deals"),

            # Calculate the total value of deals in each stage
            total_value=Sum("deals__value")
        )
        .order_by("order")
        .values(
            "name",
            "deal_count",
            "total_value"
        )
    )

    # Calculate the total value of all deals
    total_value = deals.aggregate(total=Sum("value"))["total"] or 0

    # Count all closed deals
    closed_won = deals.filter(is_closed=True).count()

    # Count deals whose due dates have passed
    overdue_count = sum(
        1
        for d in deals
        if d.is_overdue()
    )

    # Render the dashboard with all calculated statistics
    return render(
        request,
        "crm/dashboard.html",
        {
            "stage_stats": stage_stats,
            "total_value": total_value,
            "closed_won": closed_won,
            "overdue_count": overdue_count,
            "total_deals": deals.count(),
        }
    )

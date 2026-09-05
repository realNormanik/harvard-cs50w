from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.core.paginator import Paginator   # Pagination functionality   
import json # JSON functionality
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt   # CSRF exemption
from .models import *   # Import all models
from django.shortcuts import redirect

import vercel_blob
import uuid

def upload_to_blob(uploaded_file, folder=""):
    """It uploads a file to Vercel Blob in the specified folder and returns a public URL."""
    ext = uploaded_file.name.rsplit(".", 1)[-1] if "." in uploaded_file.name else ""
    filename = f"{uuid.uuid4().hex}.{ext}" if ext else uuid.uuid4().hex

    pathname = f"{folder.rstrip("/")}/{filename}" if folder else filename

    file_bytes = uploaded_file.read()

    result = vercel_blob.put(
        pathname,
        file_bytes,
        {"access": "public"}
    )
    return result["url"]


# Index route (default)
def index(request):

    if request.user.is_authenticated:
        return redirect("allPosts")

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))
    

# Create new post
@login_required(redirect_field_name="my_redirect_field")
def tweet(request):
    if request.method == "POST":
        # Get content of textarea
        form_contents = request.POST["exampleFormControlTextarea1"]
        # Get uploaded image
        image = request.FILES.get("image")

        image_url = upload_to_blob(image, folder="network/tweets") if image else None

        # Add post to database
        newTweet = Tweet(author=request.user, tweetText=form_contents, tweetImage=image_url)
        newTweet.save()

        # Redirect to all posts page
        return HttpResponseRedirect(reverse("allPosts"))
    else:
        return render(request, "network/tweet.html")


# View all posts
@login_required(redirect_field_name="my_redirect_field")
def allPosts(request):

    # Get all posts and paginate (5 posts per page)
    tweets = Tweet.objects.all().order_by("-posted")
    paginator = Paginator(tweets, 5)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # print("Debug | all tweets:",tweets)

    return render(request, "network/allPosts.html", {
        "page_obj": page_obj
    })


# View user profile and their posts
@login_required(redirect_field_name="my_redirect_field")
def profile(request, user_id):
    # Get profile
    profile = get_object_or_404(User, id=user_id)

    # Check if user follows profile
    following_status = Follow.objects.filter(user=profile, followed_by=request.user).exists()

    # Handle profile picture upload
    if request.method == "POST" and "profile_picture" in request.FILES:
        if request.user == profile:
            uploaded_picture = request.FILES["profile_picture"]
            profile.profile_picture = upload_to_blob(uploaded_picture, folder="network/profiles")
            profile.save()
            return HttpResponseRedirect(reverse("profile", args=[user_id]))

    # Get list of IDs of people the logged in user follows (Follow objects)
    following_count = profile.foo.all().count()
    followed_by_count = Follow.objects.filter(user=profile).aggregate(count=models.Count("followed_by"))["count"]

    # Gets posts from profile in reverse chronological order
    tweets = Tweet.objects.filter(author=profile).order_by("-posted")
    paginator = Paginator(tweets, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Renderuj szablon
    return render(request, "network/profile.html", {
        "page_obj": page_obj,
        "viewed_profile": profile,
        "viewed_profile_id": user_id,
        "following": following_count,
        "followedBy": followed_by_count,
        "following_status": following_status
    })


# Displays posts from profiles user is following
@login_required(redirect_field_name="my_redirect_field")
def following(request):

    # Gets all profiles user follows
    usersFollowed = request.user.following.all()
  
    # Make list of IDs
    usersFollowedIds = []
    for x in usersFollowed:
        usersFollowedIds.append(x.user.id)

    # print("Debug | User follows: ", usersFollowedIds)
    
    # Gets posts from profiles in reverse chronological order
    tweets = Tweet.objects.filter(author__in=usersFollowedIds).order_by("-posted")
    
    paginator = Paginator(tweets, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "page_obj": page_obj
    })


# Log user in
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


# Log user out
@login_required(redirect_field_name="my_redirect_field")
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# Register a new user
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        
        user.backend = "django.contrib.auth.backends.ModelBackend"
        login(request, user)
        
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


# API function: follow / unfollow profile
@login_required(redirect_field_name="my_redirect_field")
def follow(request, user_id):
    # Get current user
    user = request.user

    # Get profile being followed
    profile = get_object_or_404(User, pk=user_id)

    # Check if user is already following the profile
    follow_instance, created = Follow.objects.get_or_create(user=profile)

    if user in follow_instance.followed_by.all():
        # If already following, unfollow
        follow_instance.followed_by.remove(user)
        user.following.remove(follow_instance)
    else:
        # If not following, follow
        follow_instance.followed_by.add(user)
        user.following.add(follow_instance)

    return JsonResponse({"message": "Profile successfully followed / unfollowed"}, status=201)


# API function: Edit post
@csrf_exempt
@login_required(redirect_field_name="my_redirect_field")
def edit(request, post_id):

    # print("Debug | Edit function, post: ", post_id)
 
    # Get original post
    tweet = Tweet.objects.get(pk=post_id)

    # Gets new text (edited) in JSON format
    data = json.loads(request.body)
    new_text = data.get("tweet", "t")
    
    # Update post to new text
    tweet.tweetText = new_text
    tweet.save()

    # Return new text for instant display
    return JsonResponse({"message": "Post successfully edited", "new_text": new_text}, status=201)

@csrf_exempt
@login_required
def delete_post(request, post_id):
    if request.method != "DELETE":
        return JsonResponse({"error": "Invalid HTTP method. Use DELETE."}, status=405)

    post = get_object_or_404(Tweet, id=post_id)

    if request.user != post.author:
        return JsonResponse({"error": "You are not authorized to delete this post."}, status=403)

    post.delete()
    return JsonResponse({"message": "Post deleted successfully."}, status=200)

# API function: Like post
@csrf_exempt
@login_required(redirect_field_name="my_redirect_field")
def like(request, post_id):

    # Debug: print("Debug | Like function")

    # Get user and relevant post
    user = User.objects.get(id=request.user.id)
    tweet = Tweet.objects.get(id=post_id)

    # If user likes post unlike (and vice versa)
    if user in tweet.like.all():
        print("Debug | User already likes this post - unliking now")
        tweet.like.remove(user)

    else:
        print("Debug: user does not yet like this post - liking now")
        tweet.like.add(user)

    return JsonResponse({"message": "Post successfully liked / disliked"})
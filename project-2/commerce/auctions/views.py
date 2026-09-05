from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

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

from .models import User, AuctionListing, Bid, Comment
from .forms import AuctionListingForm, CommentForm


def index(request):
    return render(request, "auctions/index.html", {
        "listings": AuctionListing.objects.all().order_by("-created_at")
    })


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


User = get_user_model()

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })

        user.backend = "django.contrib.auth.backends.ModelBackend"
        login(request, user)

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")



@login_required
def create(request):
    return render(request, "auctions/create.html", {
        "form": AuctionListingForm()
    })


@login_required
def insert(request):
    if request.method == "POST":
        form = AuctionListingForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.cleaned_data.get("image")
            if uploaded_image:
                image_url = upload_to_blob(uploaded_image, folder="commerce/auctions")
            else:
                image_url = "/static/auctions/placeholder.webp"

            auction = AuctionListing(
                user=request.user,
                title=form.cleaned_data["title"],
                category=form.cleaned_data["category"],
                price=form.cleaned_data.get("price"),
                starting_bid=form.cleaned_data["starting_bid"],
                description=form.cleaned_data["description"],
                image=image_url
            )
            auction.save()
            bid = Bid(amount=auction.starting_bid, user=request.user, auction=auction)
            bid.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create.html", {
                "form": form,
                "error": form.errors
            })
    else:
        return render(request, "auctions/create.html", {
            "form": AuctionListingForm()
        })



def listing(request, id):
    auction = get_object_or_404(AuctionListing, pk=id)

    bids = Bid.objects.filter(auction=auction).order_by("-created_at")
    if bids.exists():
        bid = bids.first()
    else:
        bid = None

    comments = Comment.objects.filter(auction=auction)
    return render(request, "auctions/listing.html", {
        "auction": auction,
        "bid": bid,
        "comments": comments,
        "comment_form": CommentForm()
    })



@login_required
def update_bid(request, id):
    try:
        amount = float(request.POST["bid"])
        auction = get_object_or_404(AuctionListing, id=id)
        current_bid = Bid.objects.filter(auction=auction).latest("created_at")

        if amount > current_bid.amount:
            new_bid = Bid(user=request.user, amount=amount, auction=auction)
            new_bid.save()
            auction.bid_counter += 1
            auction.save()
            return HttpResponseRedirect(reverse("listing", kwargs={"id": id}))
        else:
            return render(request, "auctions/listing.html", {
                "auction": auction,
                "message": "Bid must be greater than the current bid."
            })
    except ValueError:
        return render(request, "auctions/listing.html", {
            "message": "Invalid bid value."
        })


@login_required
def close_bid(request, id):
    auction = get_object_or_404(AuctionListing, id=id)
    auction.active = False
    highest_bid = Bid.objects.filter(auction=auction).order_by("-amount").first()
    auction.winner = highest_bid.user.username if highest_bid else None
    auction.save()
    return HttpResponseRedirect(reverse("listing", kwargs={"id": id}))


@login_required
def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "watchlist": request.user.watchlist.all()
    })


@login_required
def watch(request, id):
    auction = get_object_or_404(AuctionListing, id=id)
    request.user.watchlist.add(auction)
    request.user.watchlist_counter = request.user.watchlist.count()
    request.user.save()
    return HttpResponseRedirect(reverse("listing", kwargs={"id": id}))


@login_required
def unwatch(request, id):
    auction = get_object_or_404(AuctionListing, id=id)
    request.user.watchlist.remove(auction)
    request.user.watchlist_counter = request.user.watchlist.count()
    request.user.save()
    return HttpResponseRedirect(reverse("listing", kwargs={"id": id}))


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": AuctionListing.objects.values_list("category", flat=True).distinct()
    })


def filter(request):
    category = request.GET.get("category", "").lower()
    listings = AuctionListing.objects.filter(category=category)
    return render(request, "auctions/category.html", {
        "listings": listings,
        "category": category.capitalize()
    })


@login_required
def add_comment(request, id):
    auction = get_object_or_404(AuctionListing, id=id)
    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.cleaned_data.get("image")
            image_url = upload_to_blob(uploaded_image, folder="commerce/comments") if uploaded_image else None

            comment = Comment(
                user=request.user,
                auction=auction,
                text=form.cleaned_data["text"],
                image=image_url
            )
            comment.save()
            return HttpResponseRedirect(reverse("listing", kwargs={"id": id}))
    else:
        form = CommentForm()
    return render(request, "auctions/listing.html", {
        "auction": auction,
        "comment_form": form,
        "message": "Invalid comment."
    })
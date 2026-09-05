from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Additional fields for the user
    watchlist_counter = models.IntegerField(default=0, blank=True)
    watchlist = models.ManyToManyField("AuctionListing", related_name="watchlist", blank=True)
    pass


class AuctionListing(models.Model):
    # Auction listing attributes
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Creator of the listing
    title = models.CharField(max_length=100)  # Title of the listing
    description = models.TextField()  # Description of the item
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Optional price
    starting_bid = models.DecimalField(max_digits=12, decimal_places=2, blank=True)  # Initial bid
    category = models.CharField(max_length=100, blank=True)  # Optional category
    image = models.URLField(max_length=500, blank=True, null=True)  # Image URL
    bid_counter = models.IntegerField(default=1)  # Number of bids
    created_at = models.DateTimeField(auto_now_add=True)  # Creation date
    active = models.BooleanField(default=True)  # Active status
    winner = models.CharField(max_length=100, blank=True, null=True)  # Winner of the auction

    def __str__(self):
        return f"{self.title}: by {self.user.username}"


class Bid(models.Model):
    # Bid attributes
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Bidder
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True)  # Bid amount
    created_at = models.DateTimeField(auto_now=True)  # Bid creation date
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)  # Associated auction listing

    def __str__(self):
        return f"{self.amount} on {self.auction} by {self.user.username}"


class Comment(models.Model):
    # Comment attributes
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Commenter
    text = models.TextField(blank=True)  # Comment content
    created_at = models.DateTimeField(auto_now_add=True)  # Comment creation date
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)  # Associated auction listing
    image = models.URLField(max_length=500, blank=True, null=True) # Upload media

    def __str__(self):
        return f"{self.user}: {self.text}"
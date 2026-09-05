from django.contrib import admin
from .models import User, AuctionListing, Comment, Bid

# Customize the header of the Django admin site
admin.site.site_header = "Auction's Site Administration"

# Admin configuration for the AuctionListing model
class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "price", "starting_bid", "created_at")
    # Display specific fields in the admin listing for AuctionListing

# Admin configuration for the Bid model
class BidAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "auction", "created_at")
    # Display specific fields in the admin listing for Bid

# Admin configuration for the Comment model
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "text", "auction", "created_at")
    # Display specific fields in the admin listing for Comment

# Register models with their respective admin configurations
admin.site.register(AuctionListing, AuctionListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(User)
from django.forms import ModelForm, Textarea, HiddenInput
from .models import Listing, WatchlistItem, Bid, Comment


# to create a new Listing
class NewListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "starting_bid", "image_link", "category"]
        widgets = {
            "description": Textarea(attrs={
                "class": "responsive-text-area"
            })
        }   


# To add or remove from Watchlist
class WatchListForm(ModelForm):
    class Meta:
        model = WatchlistItem
        fields = ["listing"]
        widgets = {"listing": HiddenInput()}


# to submit a Bid
class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ["amount"]
        labels = {"amount": "Enter bid"}


# to close a Listing
class CloseForm(ModelForm):
    class Meta:
        model = Listing
        fields = ["closed"]
        widgets = {"closed": HiddenInput()}


# to Comment on a Listing
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": Textarea(attrs={
                    "class": "responsive-text-area"
            })
        }

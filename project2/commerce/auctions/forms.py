from django import forms
from django.forms import ModelForm
from .models import Listing

# class NewListingForm(forms.Form):
#     title = forms.CharField(label="Listing Title")
#     description = forms.CharField(label="Listing Description",
#             widget=forms.Textarea(attrs={
#                 "class": "responsive-text-area"
#             })
#     )
#     starting_bid = forms.IntegerField(label="Starting Bid", min_value=1, 
#             max_value=2147483647)
#     image_link = forms.URLField(label="Listing Image URL", required=False)
#     category = forms.ChoiceField(label="Listing Category", required=False,
#             choices="")
    
class NewListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "starting_bid", "image_link", "category"]
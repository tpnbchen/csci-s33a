from django import forms


class NewListingForm(forms.Form):
    title = forms.CharField(label="Listing Title")
    description = forms.CharField(label="Listing Description",
            widget=forms.Textarea(attrs={
                "class": "responsive-text-area"
            })
    )
    starting_bid = forms.IntegerField(min_value=1, max_value=2147483647)
    image_link = forms.URLField(label="Listing Image URL", required=False)
from django import forms
from .models import Collection


# class CollectionForm(forms.ModelForm):
#     class Meta:
#         model = Collection
#         fields = ["collection_name", "collection_description", "collection_privacy"]


class EditCollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = [
            "collection_name",
            "collection_description",
            "collection_privacy",
            "collection_private_userlist",
        ]

        search = forms.CharField(
            required=False,
            widget=forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Search equipment..."}
            ),
        )


class CollectionFilterForm(forms.Form):
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Search collections..."}
        ),
    )

    collection_privacy = forms.ChoiceField(
        choices=[("", "All Conditions")] + Collection.LENDER_PRIVACY_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

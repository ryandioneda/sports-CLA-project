from django import forms
from .models import Equipment, Review

class EquipmentFilterForm(forms.Form):
    search = forms.CharField(required = False, widget = forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Search equipment...'
    }))

    category = forms.ChoiceField(
        choices=[('', 'All Categories')] + Equipment.CATEGORY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    condition = forms.ChoiceField(
        choices=[('', 'All Conditions')] + Equipment.CONDITION_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    min_price = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Min price'
        })
    )

    max_price = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Max price'
        })
    )

class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ["text", "rating"]
        widgets = {
            "text": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Write your review..."}),
            "rating": forms.Select(attrs={"class": "form-control"}, choices=[(i, str(i)) for i in range(1, 6)]),
        }

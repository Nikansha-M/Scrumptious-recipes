from django import forms

from recipes.models import Rating

from recipes.models import Recipe

# create a form based on Rating
class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["value"]
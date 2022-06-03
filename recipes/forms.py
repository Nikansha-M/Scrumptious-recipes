from django import forms

from recipes.models import Rating


try:
    from recipes.models import Recipe

    class RecipeForm(forms.ModelForm):
        class Meta:
            model = Recipe
            fields = [
                "name",
                "author",
                "description",
                "image",
            ]

except Exception:
    pass


# create a form based on Rating
class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["value"]
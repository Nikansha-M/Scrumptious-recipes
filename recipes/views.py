from django.shortcuts import redirect, render

from django.urls import reverse_lazy

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from recipes.forms import RatingForm


try:
    from recipes.forms import RecipeForm
    from recipes.models import Recipe
except Exception:
    RecipeForm = None
    Recipe = None


# def create_recipe(request):
#     if request.method == "POST" and RecipeForm:
#         form = RecipeForm(request.POST)
#         if form.is_valid():
#             recipe = form.save()
#             return redirect("recipe_detail", pk=recipe.pk)
#     elif RecipeForm:
#         form = RecipeForm()
#     else:
#         form = None
#     context = {
#         "form": form,
#     }
#     return render(request, "recipes/new.html", context)

class RecipeCreateView(CreateView):
    model = Recipe
    template_name = "recipes/new.html"
    fields = ["name", "author", "description", "image"]
    # after creating a new recipe, this will redirect folks 
    # back to the home page
    success_url = reverse_lazy("recipes_list")



# def change_recipe(request, pk):
#     if Recipe and RecipeForm:
#         instance = Recipe.objects.get(pk=pk)
#         if request.method == "POST":
#             form = RecipeForm(request.POST, instance=instance)
#             if form.is_valid():
#                 form.save()
#                 return redirect("recipe_detail", pk=pk)
#         else:
#             form = RecipeForm(instance=instance)
#     else:
#         form = None
#     context = {
#         "form": form,
#     }
#     return render(request, "recipes/edit.html", context)

class RecipeUpdateView(UpdateView):
    model = Recipe
    template_name = "recipes/edit.html"
    fields = ["name", "author", "description", "image"]
    success_url = reverse_lazy("recipes_list")



# def show_recipes(request):
#     context = {
#         "recipes": Recipe.objects.all() if Recipe else [],
#     }
#     return render(request, "recipes/list.html", context)

class RecipeListView(ListView):
    model = Recipe
    template_name = "recipes/list.html"
    # to add pagination to the page
    paginate_by = 3



# def show_recipe(request, pk):
#     context = {
#         "recipe": Recipe.objects.get(pk=pk) if Recipe else None,
#         # to get the RatingForm on the page
#         "rating_form": RatingForm(),
#     }
#     return render(request, "recipes/detail.html", context)

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = "recipes/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # add our form to the context dictionary using the key
        # rating_form
        context["rating_form"] = RatingForm()
        # return the contect for Django to use
        return context



def log_rating(request, recipe_id):
    if request.method == "POST":
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.recipe = Recipe.objects.get(pk=recipe_id)
            rating.save()
    return redirect("recipe_detail", pk=recipe_id)

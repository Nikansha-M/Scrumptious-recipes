from django.shortcuts import redirect

from django.urls import reverse_lazy

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin

from recipes.forms import RatingForm

# from recipes.forms import Recipe, ShoppingItem, Ingredient
from recipes.models import Recipe, ShoppingItem, Ingredient

# from django.views.decorators.http import require_http_methods
from django.db import IntegrityError


def log_rating(request, recipe_id):
    if request.method == "POST":
        form = RatingForm(request.POST)
        try:
            if form.is_valid():
                rating = form.save(commit=False)
                rating.recipe = Recipe.objects.get(pk=recipe_id)
                rating.save()
        except Recipe.DoesNotExist:
            return redirect("recipes_list")
    return redirect("recipe_detail", pk=recipe_id)


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


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    template_name = "recipes/new.html"
    fields = ["name", "description", "image", "servings"]
    # after creating a new recipe, this will redirect folks
    # back to the home page
    success_url = reverse_lazy("recipes_list")

    # assign current logged in user as the author to any recipe that is made
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


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


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipe
    template_name = "recipes/edit.html"
    fields = ["name", "description", "image", "servings"]
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

    def get_queryset(self):
        # get_queryset inheriting from ListView parent class
        query = self.request.GET.get("q")
        if not query:
            # user input should be a string
            query = ""
        # from our listof all the recipes, filter out through our description
        # to see if it matches the query

        return Recipe.objects.filter(
            description__icontains=query,
        )


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

        # create a new empty foods list
        foods = []

        # for each item in user's shopping items
        for item in self.request.user.shopping_items.all():
            # add shopping item's food to the list
            foods.append(item.food_item)
        
        context["servings"] = self.request.GET.get("servings")

        # put that list into the context
        context["food_in_shopping_list"] = foods

        # return the context for Django to use
        return context


class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipe
    template_name = "recipes/delete.html"
    success_url = reverse_lazy("recipes_list")


class ShoppingItemListView(ListView):
    model = ShoppingItem
    template_name = "shopping_items/list.html"
    paginate_by = 3

    # filter shoppint items by logged in user
    def get_queryset(self):
        return ShoppingItem.objects.filter(user=self.request.user)


# # this view only handles HTTP POST requests
# @require_http_methods(["POST"])
def create_shopping_item(request):

    # get value of ingredient_id from the request.POST dictionary
    ingredient_id = request.POST.get("ingredient_id")

    # get specific ingredient from the ingredient model
    ingredient = Ingredient.objects.get(id=ingredient_id)

    # get the current user
    user = request.user
    try:
        # create the new shopping item in the database
        ShoppingItem.objects.create(food_item=ingredient.food, user=user)
    # catch the error if ingredient is saved in the database
    except IntegrityError:
        # don't do anything with the error
        pass

    # return to recipe page with a redirect
    return redirect("recipe_detail", pk=ingredient.recipe.id)


def delete_all_shopping_items(request):
    # delete all shopping item for the logged in user
    ShoppingItem.objects.filter(user=request.user).delete()
    return redirect("shopping_item_list")
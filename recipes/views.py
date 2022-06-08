from django.shortcuts import redirect

from django.urls import reverse_lazy

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin

from recipes.forms import RatingForm

# from recipes.forms import RecipeForm
from recipes.models import Recipe


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
    fields = ["name", "description", "image"]
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

    def get_queryset(self):
        # get_queryset inheriting from ListView parent class
        query = self.request.GET.get("q")
        if not query:
            # user input should be a string
            query = ""
        # from our listof all the recipes, filter out through our description to see if it matches the query
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
        # return the contect for Django to use
        return context



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



class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipe
    template_name = "recipes/delete.html"
    success_url = reverse_lazy("recipes_list")
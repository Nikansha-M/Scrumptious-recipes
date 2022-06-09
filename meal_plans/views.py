from django.shortcuts import redirect

from django.urls import reverse_lazy

from meal_plans.models import MealPlan

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class MealPlanListView(LoginRequiredMixin, ListView):
    model = MealPlan
    template_name = "meal_plans/list.html"
    paginate_by = 3

    def get_queryset(self):
        return MealPlan.objects.filter(owner=self.request.user)


class MealPlanCreateView(LoginRequiredMixin, CreateView):
    model = MealPlan
    template_name = "meal_plans/create.html"
    fields = ["name", "date", "recipes"]
    success_url = reverse_lazy("mealplans_detail")

    def form_valid(self, form):
        plan = form.save(commit=False)
        plan.owner = self.request.user
        plan.save()
        form.save_m2m()
        return redirect("mealplans_detail", pk=plan.id)


class MealPlanDetailView(LoginRequiredMixin, DetailView):
    model = MealPlan
    template_name = "meal_plans/detail.html"

    def get_queryset(self):
        return MealPlan.objects.filter(owner=self.request.user)


class MealPlanUpdateView(LoginRequiredMixin, UpdateView):
    model = MealPlan
    template_name = "meal_plans/edit.html"
    fields = ["name", "date", "recipes"]
    
    def get_success_url(self) -> str:
        return reverse_lazy("mealplans_detail", args=[self.object.id])
    
    def get_queryset(self):
        return MealPlan.objects.filter(owner=self.request.user)


class MealPlanDeleteView(LoginRequiredMixin, DeleteView):
    model = MealPlan
    template_name = "meal_plans/delete.html"
    success_url = reverse_lazy("mealplans_list")

    def get_queryset(self):
        return MealPlan.objects.filter(owner=self.request.user)
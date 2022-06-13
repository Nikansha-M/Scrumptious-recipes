from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from django.conf import settings

USER_MODEL = settings.AUTH_USER_MODEL

# Create your models here.


# class Recipe -- we're going to inherit from models.Model
class Recipe(models.Model):
    name = models.CharField(max_length=125)
    author = models.ForeignKey(
        USER_MODEL,
        related_name="recipes",
        on_delete=models.CASCADE,
        null=True,
    )
        
    # TextField is an unlimited amount of text, no max cap
    description = models.TextField()
    
    # in our database it's going to say that it's ok if this field is empty
    # when we get to forms it's okay if this field is empty in the forms
    image = models.URLField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Measure(models.Model):
    name = models.CharField(max_length=30, unique=True)
    abbreviation = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class FoodItem(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    recipe = models.ForeignKey(
        "Recipe",
        related_name="ingredients",
        on_delete=models.CASCADE
    )
    # to limit the amount of ingredients to 20
    amount = models.FloatField(
        validators=[MinValueValidator(1),MaxValueValidator(20)],
        )
    measure = models.ForeignKey(
        "Measure",
        on_delete=models.PROTECT
    )
    food = models.ForeignKey(
        "FoodItem",
        on_delete=models.PROTECT
    )

    def __str__(self):
        return str(self.amount) + " of " + str(self.food)


class Step(models.Model):
    # author changed to recipe_name in this case is the name of the Recipe
    recipe_name = models.ForeignKey(
        "Recipe",
        # what we would like to relate to -- in this case the recipe model
        related_name="steps",
        on_delete=models.CASCADE
    )
    order = models.SmallIntegerField()
    directions = models.TextField()
    food_items = models.ManyToManyField(
        "FoodItem",
        blank=True
    )

    def __str__(self):
        return str(self.recipe_name) + " step " + str(self.order)


class Rating(models.Model):
    value = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1),MaxValueValidator(5)]
    )
    recipe = models.ForeignKey(
        "Recipe",
        related_name="ratings",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.recipe) + " rating: " + str(self.value)


class ShoppingItem(models.Model):
    user = models.ForeignKey(
        USER_MODEL,
        related_name="shopping_items",
        on_delete=models.CASCADE,
        null=True,
    )
    food_item = models.ForeignKey(
        "FoodItem",
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return f"{self.food_item} for {self.user}"
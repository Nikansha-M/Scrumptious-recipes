from django.db import models


# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=20)
    recipes = models.ManyToManyField(
        # add recipes.Recipe since they're in a different app
        "recipes.Recipe", 
        related_name="tags"
    )

    def __str__(self):
        return self.name

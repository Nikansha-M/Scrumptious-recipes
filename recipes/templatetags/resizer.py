from django import template

register = template.Library()


def resize_to(ingredient, target):
    # Get the number of servings from the ingredient's
    # recipe using the ingredient.recipe.servings
    # properties
    num_servings = ingredient.recipe.servings
    # If the servings from the recipe is not None
    #   and the value of target is not None
    if num_servings is not None and target is not None:
        # try
            # calculate the ratio of target over
            #   servings
            # return the ratio multiplied by the
            #   ingredient's amount
        try:
            calc = int(target) / int(num_servings)
            return calc * ingredient.amount
        # catch a possible error
            # pass
        except ValueError:
            pass
        # return the original ingredient's amount since
        # no thing else worked
        return ingredient.amount

    # print("value:", value)
    # print("arg:", arg)
    # return "resize done"


register.filter(resize_to)
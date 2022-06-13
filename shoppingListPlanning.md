Users only need a single shopping list.

# The MVP for this project is four features:

    1. A "+ shopping list" button next to any ingredient not already in the shopping list that, when clicked, adds it to the shopping list

    2. A main nav link that links to a list of the current items in the shopping list with an indicator of how many items are in the shopping list

    3. The actual shopping list of food items that have been added

    4. A button and view on the list page to clear all items from the shopping list

    5. Each user has their own shopping list


### Requirements:

    3. user should only be able to add one FoodItem once to their shopping list (to avoid duplicates of the same FoodItem)

    4. user can have many shopping lists (one-to-many relationship)


### Exceptions: Two Features in this project that **require** the use of function views

    1. the view to clear the shopping list by deleting all of the shopping items; the DeleteView is really only good for deleting a single item

    2. the view to add an ingredient's food item to the shopping list because when we show it, it's not a normal form


#### In Django App

    1.  recipes/Models.py & recipes/admin.py
        [x] create and register **ShoppingItem Model**
                user = 
                    AUTH_USER_MODEL
                    foreign key to the Django user model, cascade on delete

                food_item = 
                    "FoodItem"
                    foreign key to FoodItem, protect on delete
    

    2.  Recipes/Views.py
        [x] Create the class ShoppingItemListView
        []  Create the class ShoppingItemCreateView
        []  Create the class ShoppingItemDeleteView
    
    
    3.  Create the paths in recipes/urls.py
        [x]  Add a shopping item to the user's shopping list: _recipes/shopping_items/create/_
        [x]  Show the list of shopping items on the user's shopping list: _recipes/shopping_items/_	
        [x]  Remove all shopping items from a user's shopping list: _recipes/shopping_items/delete/_	
    
    
    4.  HTML
            Base:   
            [x]  add Shopping List to Nav Bar
            [x]  change shopping_items url

            List:
            []  button to delete ALL items from user's shopping list
            []  show a list of shopping items that was created by the user

            Create:
            []  no html template

            Delete:
            []  no html template


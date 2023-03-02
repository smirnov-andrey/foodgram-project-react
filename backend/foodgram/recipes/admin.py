from django.contrib import admin

from .models import *

admin.site.register(Ingredient)
admin.site.register(IngredientInRecipe)
admin.site.register(Tag)
admin.site.register(Recipe)
admin.site.register(FavoriteRecipes)
admin.site.register(ShoppingCarts)


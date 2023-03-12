from django.contrib import admin

from .models import (FavoriteRecipes, Ingredient, IngredientInRecipe, Recipe,
                     ShoppingCarts, Tag)


class RecipeToIngredientInline(admin.TabularInline):
    model = IngredientInRecipe
    list_display = ('recipe', 'amount')
    readonly_fields = ('recipe', 'amount')
    search_fields = ('recipe__name', 'recipe__author__name')
    can_delete = False
    extra = 0


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_display_links = ('id', 'name')
    list_filter = ('measurement_unit',)
    ordering = ('name',)
    search_fields = ('name', 'measurement_unit')
    search_help_text = 'Поиск по названию ингридиента и/или единицам измерения'
    actions_selection_counter = True
    show_full_result_count = True
    inlines = (RecipeToIngredientInline,)


class IngredientToRecipeInline(admin.TabularInline):
    model = IngredientInRecipe
    search_fields = ('ingredient__name', 'ingredient__measurement_unit')
    autocomplete_fields = ('ingredient',)
    show_change_link = False
    can_delete = False
    extra = 0


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author')
    list_display_links = ('id', 'name')
    search_fields = ('name', )
    actions_selection_counter = True
    autocomplete_fields = ('author',)
    inlines = (IngredientToRecipeInline,)


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'color')
    list_display_links = ('id', 'name', 'slug')
    prepopulated_fields = {"slug": ("name",)}


class FavoriteRecipesAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    list_display_links = ('id', 'user', 'recipe')
    autocomplete_fields = ('user', 'recipe')
    actions_selection_counter = True
    search_fields = ('user', 'recipe')


class ShoppingCartsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    list_display_links = ('id', 'user', 'recipe')
    autocomplete_fields = ('user', 'recipe')
    actions_selection_counter = True
    search_fields = ('user', 'recipe')


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(FavoriteRecipes, FavoriteRecipesAdmin)
admin.site.register(ShoppingCarts, ShoppingCartsAdmin)

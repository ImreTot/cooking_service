from django.contrib import admin

from .models import Tag, Ingredient, Recipe

admin.site.register(Tag)
admin.site.register(Ingredient)


class IngredientInlineAdmin(admin.TabularInline):
    model = Recipe.ingredients.through


class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientInlineAdmin,)


admin.site.register(Recipe, RecipeAdmin)

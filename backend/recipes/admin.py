from django.contrib import admin

from .models import (Tag, Ingredient, Recipe, RecipeIngredient,
                     Subscription)

admin.site.register(Tag)
admin.site.register(Subscription)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,)


class IngredientAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline, )


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(RecipeIngredient)

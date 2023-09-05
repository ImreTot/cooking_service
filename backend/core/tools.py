import os
from django.conf import settings
from django.http import HttpResponse
from rest_framework.generics import get_object_or_404
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from recipes.models import Recipe

def get_user_and_recipe_or_404(request, pk):
    user = request.user
    recipe = get_object_or_404(Recipe, id=pk)
    return user, recipe

def generate_ingredients_list_via_pdf(ingredient_list):
    font_path = os.path.join(settings.FONT_ROOT, 'Zekton.ttf')
    pdfmetrics.registerFont(
        TTFont(name='Zekton', filename=font_path, validate='UTF-8'))
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = ('attachment; '
                                       'filename="shopping_list.pdf"')
    page = canvas.Canvas(response)
    page.setFont('Zekton', size=24)
    page.drawString(200, 800, 'Список ингредиентов')
    page.setFont('Zekton', size=16)
    height = 750
    for i, (name, data) in enumerate(ingredient_list.items(), 1):
        page.drawString(75, height, (f'{i}. {name} - {data["amount"]}, '
                                     f'{data["measurement_unit"]}'))
        height -= 25
    page.showPage()
    page.save()
    return response

def form_ingredients_list(queryset):
    ingredient_list = {}
    for item in queryset:
        name = item[0]
        if name not in ingredient_list:
            ingredient_list[name] = {
                'measurement_unit': item[1],
                'amount': item[2]
            }
        else:
            ingredient_list[name]['amount'] += item[2]
    print(ingredient_list)
    return ingredient_list
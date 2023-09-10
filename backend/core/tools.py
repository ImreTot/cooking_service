import os

from django.conf import settings
from django.http import HttpResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework.generics import get_object_or_404

from recipes.models import Recipe

FONT_SIZE = 24
HEIGHT = 750
HEADER_LENGTH = 200
HEADER_HEIGHT = 800
TEXT_SIZE = 16
LENGTH = 75


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
    page.setFont('Zekton', size=FONT_SIZE)
    page.drawString(HEADER_LENGTH, HEADER_HEIGHT, 'Список ингредиентов')
    page.setFont('Zekton', size=TEXT_SIZE)
    height = HEIGHT
    for i, (name, data) in enumerate(ingredient_list.items(), 1):
        page.drawString(LENGTH, height, (f'{i}. {name} - {data["amount"]}, '
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
    return ingredient_list

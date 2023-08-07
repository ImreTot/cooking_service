from django.core.validators import RegexValidator, MinValueValidator
from django.contrib.auth import get_user_model
from django.db import models

UNIT_CHOICES = (
    ('кг', 'кг'),
    ('г', 'г'),
    ('мл', 'мл'),
    ('л', 'л'),
    ('шт', 'шт'),
)

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    color = models.CharField(max_length=7, unique=True)
    slug = models.SlugField(max_length=200,
                            unique=True,
                            validators=[
                               RegexValidator(
                                   regex=r'^[-a-zA-Z0-9_]+$',
                                   message='Invalid slug.'
                               )
                            ])

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200,
                                        choices=UNIT_CHOICES)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='recipes')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='RecipeIngredient',
                                         related_name='recipes')
    tags = models.ManyToManyField(Tag, related_name='recipes')
    image = models.ImageField(upload_to='recipes/')
    name = models.CharField(max_length=200)
    text = models.TextField()
    cooking_time = models.PositiveIntegerField(validators=[
        MinValueValidator(limit_value=1, message='Too little time.')
    ])
    publication_date = models.DateTimeField(auto_now_add=True,
                                            db_index=True)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=6, decimal_places=2)
    unit = models.CharField(max_length=10)


class Subscription(models.Model):
    user = models.ForeignKey(User,
                             related_name='follower',
                             on_delete=models.CASCADE)
    author = models.ForeignKey(User,
                               related_name='following',
                               on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'],
                                    name='unique_subscription')
        ]


class Favorite(models.Model):
    user = models.ForeignKey(User,
                             related_name='favourites',
                             on_delete=models.CASCADE)
    recipe = models.ForeignKey(User,
                               related_name='subscribers',
                               on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_favorite')
        ]

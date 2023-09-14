from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator, MaxValueValidator
from django.db import models

MIN_VALUE = 1
MAX_VALUE = 32000

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    color = ColorField()
    slug = models.SlugField(max_length=200,
                            unique=True,
                            validators=[
                                RegexValidator(
                                    regex=r'^[-a-zA-Z0-9_]+$',
                                    message='Invalid slug.'
                                )
                            ])

    class Meta:
        ordering = ['slug']

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(blank=True,
                                        null=True,
                                        max_length=200)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='recipes')
    tags = models.ManyToManyField(Tag, related_name='recipes')
    image = models.ImageField(upload_to='recipes/')
    name = models.CharField(max_length=200)
    text = models.TextField()
    cooking_time = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(limit_value=MIN_VALUE,
                          message='Too short a period of time.'),
        MaxValueValidator(limit_value=MAX_VALUE,
                          message='Too long a period of time.')
    ])
    publication_date = models.DateTimeField(auto_now_add=True,
                                            db_index=True)

    class Meta:
        ordering = ['-publication_date']

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='ingredients')
    ingredient = models.ForeignKey(Ingredient,
                                   related_name='recipes',
                                   on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        validators=[
            MaxValueValidator(limit_value=MAX_VALUE,
                              message='Amount value is too high.'),
            MinValueValidator(limit_value=MIN_VALUE,
                              message='Amount value is too small')
        ])

    class Meta:
        ordering = ['-recipe']


class Subscription(models.Model):
    follower = models.ForeignKey(User,
                                 related_name='subscriptions',
                                 on_delete=models.CASCADE)
    following = models.ForeignKey(User,
                                  related_name='subscribers',
                                  on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['follower', 'following'],
                                    name='unique_subscription')
        ]
        ordering = ['-follower']


class Favorite(models.Model):
    user = models.ForeignKey(User,
                             related_name='favorite_recipes',
                             on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe,
                               related_name='favorited_by',
                               on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['user', 'recipe'],
            name='unique_favorite'
        )]
        ordering = ['-user']


class ShoppingCart(models.Model):
    user = models.ForeignKey(User,
                             related_name='recipes_in_shopping_cart',
                             on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe,
                               related_name='shopping_by',
                               on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['user', 'recipe'],
            name='unique_recipe_for_shopping'
        )]
        ordering = ['-user']

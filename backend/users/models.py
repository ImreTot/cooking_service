from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator


class User(AbstractUser):
    email = models.EmailField('email address',
                              max_length=254,
                              unique=True)
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text=(f'Required. '
                   f'150 characters or fewer. '
                   f'Letters, digits and @/./+/-/_ only.'),
        validators=[UnicodeUsernameValidator],
        error_messages={
            'unique': 'A user with that username already exists.',
        }
    )
    first_name = models.CharField('first name', max_length=150)
    last_name = models.CharField('last name', max_length=150)

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

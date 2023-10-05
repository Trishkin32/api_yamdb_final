"""User class models."""
from django.contrib.auth.models import AbstractUser
from django.db import models

from users.validators import ValidateUsername

USER_ROLE = 'user'
MODERATOR_ROLE = 'moderator'
ADMIN_ROLE = 'admin'

CHOICES_ROLE = (
    (USER_ROLE, 'User'),
    (MODERATOR_ROLE, 'Moderator'),
    (ADMIN_ROLE, 'Admin'),
)


class User(ValidateUsername, AbstractUser):
    """Own user class for yamdb project."""

    email = models.EmailField(
        unique=True,
    )
    bio = models.TextField(
        verbose_name='biography',
        blank=True,
    )
    role = models.CharField(
        verbose_name='role',
        max_length=20,
        choices=CHOICES_ROLE,
        default=USER_ROLE,
    )

    class Meta:
        db_table = 'user'
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ('username',)
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_name'
            ),
            models.CheckConstraint(
                check=~models.Q(username='me'),
                name='name_not_me'
            ),
        ]

    @property
    def is_admin(self):
        return self.role == ADMIN_ROLE or self.is_superuser or self.is_staff

    @property
    def is_moderator(self):
        return self.role == MODERATOR_ROLE

    def __str__(self):
        return self.username

import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from parties.querysets import PartyQuerySet, GuestQuerySet


class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True
    )

    objects = UserManager()

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'


class Party(BaseModel):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        related_name='+',
        on_delete=models.PROTECT,
    )
    is_public = models.BooleanField(default=True)

    objects = PartyQuerySet.as_manager()

    def __str__(self):
        return self.name


class Guest(BaseModel):
    name = models.CharField(max_length=100)
    birth_date = models.DateField(auto_now_add=False)
    party = models.ForeignKey(
        to='parties.Party',
        related_name='guests',
        on_delete=models.CASCADE,
    )
    owner = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        related_name='+',
        on_delete=models.PROTECT,
    )

    objects = GuestQuerySet.as_manager()

    def __str__(self):
        return self.name

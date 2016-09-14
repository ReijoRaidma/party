from django.conf import settings
from django.db import models
import datetime

from parties.querysets import PartyQuerySet


class Party(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='parties')
    is_public = models.BooleanField(default=True)

    objects = PartyQuerySet.as_manager()

    def __str__(self):
        return self.name


class Guest(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField(auto_now_add=False, default=datetime.datetime.now)
    party = models.ForeignKey(Party, related_name='guests')

    def __str__(self):
        return self.name


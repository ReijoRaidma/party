from django.db import models
from django.db.models.query_utils import Q


class PartyQuerySet(models.QuerySet):
    def readable(self, user):
        return self.filter(Q(is_public=True) | Q(owner=user))


class GuestQuerySet(models.QuerySet):
    def readable(self, user):
        return self.filter(Q(owner=user) | Q(party__is_public=True))

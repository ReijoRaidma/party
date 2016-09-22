from django.db import models
from django.db.models.query_utils import Q


class PartyQuerySet(models.QuerySet):
    def readable(self, user):
        if user.is_authenticated:
            if user.is_superuser:
                return self
            else:
                return self.filter(Q(is_public=True) | Q(owner=user))
        else:
            return self.filter(is_public=True)


class GuestQuerySet(models.QuerySet):
    def readable(self, user):
        if user.is_authenticated:
            return self.filter(Q(owner=user) | Q(party__is_public=True))
        else:
            return self.filter(party__is_public=True)

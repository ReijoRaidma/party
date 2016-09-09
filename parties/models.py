from django.db import models
import datetime

class Party(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Guest(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField(auto_now_add=False,default=datetime.datetime.now)
    party = models.ForeignKey(Party, related_name='guests')

    def __str__(self):
        return self.name


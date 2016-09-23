
from django.forms import ModelForm

from parties.models import Party


class PartyForm(ModelForm):
    class Meta:
        model = Party
        fields = ['name', 'owner']

from django.contrib import messages
from django.db import  transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import inlineformset_factory


from parties.models import Guest, Party
from parties.forms import PartyForm


@transaction.atomic
def add_party(request):
    party_form = PartyForm(request.POST or None)
    GuestFormSet = inlineformset_factory(Party, Guest, fields=('name', 'birth_date'),extra=1)
    formset = GuestFormSet(request.POST or None)

    if request.method == 'POST':
        if all([party_form.is_valid(), formset.is_valid()]):
            party = party_form.save()
            for guest_form in formset:
                guest = guest_form.save(commit=False)
                guest.party = party
                guest.save()
            messages.success(request, "Added guests")
            return redirect('parties:party_list')

    return render(request, 'add_party.html', {
        'party_form': party_form,
        'guest_formset': formset,
    })


@transaction.atomic
def edit_party(request, pk):
    party = get_object_or_404(Party, pk=pk)
    party_form = PartyForm(request.POST or None, instance=party)

    GuestFormSet = inlineformset_factory(Party, Guest, fields=('name', 'birth_date'),extra=0)
    formset = GuestFormSet(request.POST or None, instance=party)

    if request.method == 'POST':
        if all([party_form.is_valid(), formset.is_valid()]):
            party_form.save()
            formset.save()
            messages.success(request, 'updated')
            return redirect('parties:party_list')

    return render( request, 'edit_party.html', {
        'party_form': party_form,
        'formset': formset,
        'party': party
    })


def party_list(request):
    parties = Party.objects.all()
    return render(request, 'party_list.html', {
        'parties': parties
    })


def party_detail(request, pk):
    party = get_object_or_404(Party, pk=pk)

    return render(request, 'party_detail.html', {

        'party': party
    })
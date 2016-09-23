from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import transaction
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect, get_object_or_404

from rest_framework import filters
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from parties.models import Guest, Party
from parties.forms import PartyForm
from parties.serializers import PartySerializer, GuestSerializer, UserSerializer
from parties.permissions import ObjectOwnerPermission, UserPermission

# API Views


class GuestViewSet(viewsets.ModelViewSet):
    permission_classes = (ObjectOwnerPermission, IsAuthenticatedOrReadOnly)
    queryset = Guest.objects.none()
    serializer_class = GuestSerializer

    def get_queryset(self):
        return Guest.objects.readable(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PartyViewSet(viewsets.ModelViewSet):
    permission_classes = (ObjectOwnerPermission, IsAuthenticatedOrReadOnly)
    queryset = Party.objects.none()
    serializer_class = PartySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def get_queryset(self):
        return Party.objects.readable(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (UserPermission, IsAuthenticatedOrReadOnly,)
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

# Django views


@transaction.atomic
def add_party(request):
    party_form = PartyForm(request.POST or None)
    GuestFormSet = inlineformset_factory(Party, Guest, fields=('name', 'birth_date'), extra=1)
    formset = GuestFormSet(request.POST or None)

    if request.method == 'POST':
        if all([party_form.is_valid(), formset.is_valid()]):
            party = party_form.save()
            for guest_form in formset:
                guest = guest_form.save(commit=False)
                guest.party = party
                guest.save()
            messages.success(request, "Added guests")
            return redirect('party_list')

    return render(request, 'add_party.html', {
        'party_form': party_form,
        'guest_formset': formset,
    })


@transaction.atomic
def edit_party(request, pk):
    party = get_object_or_404(Party, pk=pk)
    party_form = PartyForm(request.POST or None, instance=party)

    GuestFormSet = inlineformset_factory(Party, Guest, fields=('name', 'birth_date'), extra=1)
    formset = GuestFormSet(request.POST or None, instance=party)

    if request.method == 'POST':
        if all([party_form.is_valid(), formset.is_valid()]):
            party_form.save()
            formset.save()
            messages.success(request, 'updated')
            return redirect('party_list')

    return render(request, 'edit_party.html', {
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

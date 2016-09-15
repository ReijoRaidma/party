from django.contrib import messages
from django.contrib.auth.models import User
from django.db import transaction
from django.forms import inlineformset_factory
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from parties.models import Guest, Party
from parties.forms import PartyForm
from parties.serializers import PartySerializer, GuestSerializer, UserSerializer
from parties.permissions import IsOwnerOrReadOnly

class GuestViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwnerOrReadOnly,)
    queryset = Guest.objects.none()
    serializer_class = GuestSerializer

    def get_queryset(self):
        return Guest.objects.readable(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
#
# class GuestList(generics.ListCreateAPIView):
#     queryset = Guest.objects.all()
#     serializer_class = GuestSerializer
#
#
# class GuestDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Guest.objects.all()
#     serializer_class = GuestSerializer


class PartyViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwnerOrReadOnly,)
    queryset = Party.objects.none()
    serializer_class = PartySerializer

    def get_queryset(self):
        return Party.objects.readable(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# class ApiPartyList(generics.ListCreateAPIView):
#     queryset = Party.objects.all()
#     serializer_class = PartySerializer
#
#
#     def perform_create(self, GuestSerializer):
#         serializer.save(party=self.request.name)
#
#
# class ApiPartyDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Party.objects.all()
#     serializer_class = PartySerializer

# @api_view(['GET', 'POST'])
# def api_party_list(request, format=None):
#     if request.method == 'GET':
#         parties = Party.objects.all()
#         serializer = PartySerializer(parties, many=True)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         serializer = PartySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET','PUT','DELETE'])
# def api_party_detail(request, pk, format=None):
#     party = get_object_or_404(Party, pk=pk)
#
#     if request.method == 'GET':
#         serializer = PartySerializer(party)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         serializer = PartySerializer(party, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         party.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


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
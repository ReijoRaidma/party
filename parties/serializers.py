from django.shortcuts import get_object_or_404
from rest_framework import serializers
from parties.models import Party, Guest


class PartySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='api:party-detail',
    )
    guests = serializers.HyperlinkedRelatedField(
        view_name='api:guest-detail',
        many=True,
        read_only=True,
    )
    owner = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    class Meta:
        model = Party
        fields = (
            'id',
            'url',
            'name',
            'owner',
            'guests',
        )


class GuestSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='api:guest-detail'
    )

    class Meta:
        model = Guest
        fields = ('id','url','name', 'birth_date', 'party')




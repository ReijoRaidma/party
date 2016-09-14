from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
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
    owner = serializers.HyperlinkedRelatedField(
        view_name='api:user-detail',
        read_only=True
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
        fields = ('id', 'url', 'name', 'birth_date', 'party')


class UserSerializer(serializers.ModelSerializer):
    parties = serializers.HyperlinkedRelatedField(
        view_name='api:party-detail',
        many=True,
        read_only=True
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'parties')

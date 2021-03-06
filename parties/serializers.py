from django.contrib.auth import get_user_model
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
            'is_public',
            'guests',
        )


class GuestSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='api:guest-detail'
    )
    party = serializers.HyperlinkedRelatedField(
        view_name='api:party-detail',
        queryset=Party.objects.none()
    )
    owner = serializers.HyperlinkedRelatedField(
        view_name='api:user-detail',
        read_only=True
    )

    class Meta:
        model = Guest
        fields = (
            'id',
            'url',
            'name',
            'birth_date',
            'party',
            'owner',
        )

    def get_fields(self):
        fields = super(GuestSerializer, self).get_fields()
        fields['party'].queryset = Party.objects.readable(user=self.context.get('request').user)
        return fields


class UserSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='api:user-detail',
    )

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'url',
            'username',
            'first_name',
            'last_name',
            'email',
        )

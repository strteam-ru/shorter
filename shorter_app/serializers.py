from rest_framework import serializers

from .models import Links


class LinksSerializer(serializers.ModelSerializer):
    """save link request"""

    class Meta:
        model = Links
        fields = ('user_id', 'short_link', 'full_link')


class UserLinksSerializer(serializers.ModelSerializer):
    """save link request"""

    class Meta:
        model = Links
        fields = ('id', 'short_link', 'full_link', 'created')


class HostSerializer(serializers.Serializer):
    host = serializers.CharField()


class UserSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    page = serializers.IntegerField()


class SortLinkSerializer(serializers.Serializer):
    short_link = serializers.CharField(min_length=2, max_length=10)

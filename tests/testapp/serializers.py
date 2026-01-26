from rest_framework import serializers

from testapp.models import PrivateModel, PublicModel


class PublicModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicModel
        fields = [
            "name",
        ]


class PrivateModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateModel
        fields = [
            "name",
        ]

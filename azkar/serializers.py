from rest_framework import serializers

from .models import Azkar, AzkarCategory


class AzkarCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AzkarCategory
        fields = ("id", "title", "slug")


class AzkarSerializer(serializers.ModelSerializer):
    category = AzkarCategorySerializer(read_only=True)

    class Meta:
        model = Azkar
        fields = (
            "id",
            "category",
            "title",
            "slug",
            "arabic",
            "urdu",
            "reference",
            "time_of_day",
            "order",
        )

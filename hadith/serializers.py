from rest_framework import serializers

from .models import Hadith, HadithBook, HadithChapter


class HadithBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = HadithBook
        fields = ("id", "title", "slug")


class HadithChapterSerializer(serializers.ModelSerializer):
    book = HadithBookSerializer(read_only=True)

    class Meta:
        model = HadithChapter
        fields = ("id", "book", "number", "title", "slug")


class HadithSerializer(serializers.ModelSerializer):
    chapter = HadithChapterSerializer(read_only=True)

    class Meta:
        model = Hadith
        fields = (
            "id",
            "chapter",
            "number_in_chapter",
            "text_ar",
            "text_ur",
            "text_en",
            "grade",
            "reference",
        )

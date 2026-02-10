from rest_framework import serializers

from .models import QuranAyah, QuranSurah


class QuranSurahSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuranSurah
        fields = ("id", "number", "name_ar", "name_en", "name_ur", "slug", "ayah_count")


class QuranAyahSerializer(serializers.ModelSerializer):
    surah = QuranSurahSerializer(read_only=True)

    class Meta:
        model = QuranAyah
        fields = (
            "id",
            "surah",
            "number_in_surah",
            "text_ar",
            "translation_ur",
            "translation_en",
        )

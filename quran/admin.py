from django.contrib import admin

from .models import QuranAyah, QuranSurah


@admin.register(QuranSurah)
class QuranSurahAdmin(admin.ModelAdmin):
    list_display = ("number", "name_ar", "name_ur", "name_en", "slug", "ayah_count")
    search_fields = ("name_ar", "name_ur", "name_en", "slug")
    prepopulated_fields = {"slug": ("name_en",)}


@admin.register(QuranAyah)
class QuranAyahAdmin(admin.ModelAdmin):
    list_display = ("surah", "number_in_surah")
    list_filter = ("surah",)
    search_fields = ("text_ar", "translation_ur", "translation_en")

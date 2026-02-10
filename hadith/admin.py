from django.contrib import admin

from .models import Hadith, HadithBook, HadithChapter


@admin.register(HadithBook)
class HadithBookAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    search_fields = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(HadithChapter)
class HadithChapterAdmin(admin.ModelAdmin):
    list_display = ("book", "number", "title", "slug")
    list_filter = ("book",)
    search_fields = ("title", "slug")


@admin.register(Hadith)
class HadithAdmin(admin.ModelAdmin):
    list_display = ("chapter", "number_in_chapter", "grade")
    list_filter = ("grade", "chapter__book")
    search_fields = ("text_ar", "text_ur", "text_en", "reference")

from django.contrib import admin

from .models import Azkar, AzkarCategory


@admin.register(AzkarCategory)
class AzkarCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    search_fields = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Azkar)
class AzkarAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "time_of_day", "order")
    list_filter = ("time_of_day", "category")
    search_fields = ("title", "arabic", "urdu", "reference")

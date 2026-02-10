from django.contrib import admin

from .models import ResearchPaper


@admin.register(ResearchPaper)
class ResearchPaperAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "published_at", "slug")
    list_filter = ("author",)
    search_fields = ("title", "summary", "references", "author", "slug")
    prepopulated_fields = {"slug": ("title",)}

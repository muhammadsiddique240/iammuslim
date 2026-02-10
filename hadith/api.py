from rest_framework import viewsets

from .models import Hadith, HadithBook, HadithChapter
from .serializers import HadithBookSerializer, HadithChapterSerializer, HadithSerializer


class HadithBookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HadithBook.objects.all()
    serializer_class = HadithBookSerializer
    lookup_field = "slug"


class HadithChapterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HadithChapter.objects.select_related("book").all()
    serializer_class = HadithChapterSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        book_slug = self.request.query_params.get("book")
        if book_slug:
            qs = qs.filter(book__slug=book_slug)
        return qs


class HadithViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Hadith.objects.select_related("chapter", "chapter__book").all()
    serializer_class = HadithSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        book_slug = self.request.query_params.get("book")
        chapter_slug = self.request.query_params.get("chapter")
        if book_slug:
            qs = qs.filter(chapter__book__slug=book_slug)
        if chapter_slug:
            qs = qs.filter(chapter__slug=chapter_slug)
        return qs

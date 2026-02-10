from rest_framework import viewsets

from .models import QuranAyah, QuranSurah
from .serializers import QuranAyahSerializer, QuranSurahSerializer


class QuranSurahViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = QuranSurah.objects.all()
    serializer_class = QuranSurahSerializer
    lookup_field = "slug"


class QuranAyahViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = QuranAyah.objects.select_related("surah").all()
    serializer_class = QuranAyahSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        surah_slug = self.request.query_params.get("surah")
        if surah_slug:
            qs = qs.filter(surah__slug=surah_slug)
        return qs

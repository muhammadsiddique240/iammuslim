from rest_framework import viewsets

from .models import Azkar, AzkarCategory
from .serializers import AzkarCategorySerializer, AzkarSerializer


class AzkarCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AzkarCategory.objects.all()
    serializer_class = AzkarCategorySerializer
    lookup_field = "slug"


class AzkarViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Azkar.objects.select_related("category").all()
    serializer_class = AzkarSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        category_slug = self.request.query_params.get("category")
        time_of_day = self.request.query_params.get("time")
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        if time_of_day:
            qs = qs.filter(time_of_day=time_of_day)
        return qs

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Azkar, AzkarCategory


def category_list(request: HttpRequest) -> HttpResponse:
    categories = AzkarCategory.objects.all()
    return render(request, "azkar/category_list.html", {"categories": categories})


def category_detail(request: HttpRequest, slug: str) -> HttpResponse:
    category = get_object_or_404(AzkarCategory, slug=slug)
    items = category.items.all()
    return render(request, "azkar/category_detail.html", {"category": category, "items": items})


def morning(request: HttpRequest) -> HttpResponse:
    items = Azkar.objects.filter(time_of_day=Azkar.TimeOfDay.MORNING).select_related("category")
    return render(request, "azkar/time_of_day.html", {"title": "Morning Azkar", "items": items})


def evening(request: HttpRequest) -> HttpResponse:
    items = Azkar.objects.filter(time_of_day=Azkar.TimeOfDay.EVENING).select_related("category")
    return render(request, "azkar/time_of_day.html", {"title": "Evening Azkar", "items": items})

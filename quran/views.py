from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import QuranSurah

import json
import os
from django.http import JsonResponse, Http404
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_GET
from django.conf import settings


def surah_list(request: HttpRequest) -> HttpResponse:
    surahs = QuranSurah.objects.all()
    return render(request, "quran/surah_list.html", {"surahs": surahs})


def surah_detail(request: HttpRequest, slug: str) -> HttpResponse:
    surah = get_object_or_404(QuranSurah, slug=slug)
    page_number = request.GET.get("page", "1")
    paginator = Paginator(surah.ayahs.all(), 20)
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "quran/surah_detail.html",
        {"surah": surah, "page_obj": page_obj},
    )


@require_GET
@cache_page(60 * 60 * 24)  # Cache for 24 hours
def quran_arabic_json(request):
    """Serve complete Quran data in Arabic"""
    try:
        json_path = os.path.join(settings.BASE_DIR, 'data', 'quran_arabic.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return JsonResponse(data, safe=False)
    except FileNotFoundError:
        raise Http404("Quran Arabic data not found")
    except json.JSONDecodeError:
        raise Http404("Invalid Quran Arabic data format")


@require_GET
@cache_page(60 * 60 * 24)  # Cache for 24 hours
def quran_urdu_json(request):
    """Serve complete Quran data in Urdu"""
    try:
        json_path = os.path.join(settings.BASE_DIR, 'data', 'quran_urdu.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return JsonResponse(data, safe=False)
    except FileNotFoundError:
        raise Http404("Quran Urdu data not found")
    except json.JSONDecodeError:
        raise Http404("Invalid Quran Urdu data format")


@require_GET
@cache_page(60 * 60 * 24)  # Cache for 24 hours
def quran_surah_json(request, surah_number):
    """Serve specific Surah data from Arabic Quran"""
    try:
        json_path = os.path.join(settings.BASE_DIR, 'data', 'quran_arabic.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        surahs = data.get('quran', {}).get('surahs', [])
        for surah in surahs:
            if surah['number'] == surah_number:
                return JsonResponse(surah, safe=False)

        raise Http404(f"Surah {surah_number} not found")

    except FileNotFoundError:
        raise Http404("Quran data not found")
    except json.JSONDecodeError:
        raise Http404("Invalid Quran data format")


@require_GET
@cache_page(60 * 60 * 24)  # Cache for 24 hours
def quran_surah_urdu_json(request, surah_number):
    """Serve specific Surah data from Urdu Quran"""
    try:
        json_path = os.path.join(settings.BASE_DIR, 'data', 'quran_urdu.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        surahs = data.get('quran', {}).get('surahs', [])
        for surah in surahs:
            if surah['number'] == surah_number:
                return JsonResponse(surah, safe=False)

        raise Http404(f"Surah {surah_number} not found")

    except FileNotFoundError:
        raise Http404("Quran Urdu data not found")
    except json.JSONDecodeError:
        raise Http404("Invalid Quran Urdu data format")


@require_GET
@cache_page(60 * 60 * 24)  # Cache for 24 hours
def quran_info_json(request):
    """Serve Quran metadata and information"""
    try:
        arabic_path = os.path.join(settings.BASE_DIR, 'data', 'quran_arabic.json')
        urdu_path = os.path.join(settings.BASE_DIR, 'data', 'quran_urdu.json')

        info = {
            "quran": {
                "name": "القرآن الكريم",
                "name_english": "The Noble Quran",
                "total_surahs": 114,
                "languages_available": ["ar", "ur"],
                "api_endpoints": {
                    "arabic": "/api/quran/ar/",
                    "urdu": "/api/quran/ur/",
                    "surah_arabic": "/api/quran/ar/surah/{number}/",
                    "surah_urdu": "/api/quran/ur/surah/{number}/",
                    "info": "/api/quran/info/"
                }
            }
        }

        # Check if files exist
        info["quran"]["files_available"] = {
            "arabic": os.path.exists(arabic_path),
            "urdu": os.path.exists(urdu_path)
        }

        return JsonResponse(info, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

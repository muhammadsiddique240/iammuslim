from django.core.paginator import Paginator
from django.db import connection
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

try:
    from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

    _POSTGRES_SEARCH_AVAILABLE = True
except Exception:
    _POSTGRES_SEARCH_AVAILABLE = False

from azkar.models import Azkar
from hadith.models import Hadith
from quran.models import QuranAyah
from research.models import ResearchPaper


def home(request: HttpRequest) -> HttpResponse:
    return render(request, "core/home.html")


def global_search(request: HttpRequest) -> HttpResponse:
    query = request.GET.get("q", "").strip()
    page_number = request.GET.get("page", "1")

    ayah_qs = QuranAyah.objects.none()
    hadith_qs = Hadith.objects.none()
    azkar_qs = Azkar.objects.none()
    research_qs = ResearchPaper.objects.none()

    combined: list[tuple[str, object, float]] = []

    if query:
        use_pg_search = connection.vendor == "postgresql" and _POSTGRES_SEARCH_AVAILABLE

        if use_pg_search:
            search_query = SearchQuery(query)

            ayah_vector = SearchVector("text_ar", weight="A") + SearchVector(
                "translation_ur", weight="B"
            ) + SearchVector("translation_en", weight="C")
            ayah_qs = (
                QuranAyah.objects.select_related("surah")
                .annotate(rank=SearchRank(ayah_vector, search_query))
                .filter(rank__gt=0)
                .order_by("-rank")
            )

            hadith_vector = (
                SearchVector("text_ar", weight="A")
                + SearchVector("text_ur", weight="B")
                + SearchVector("text_en", weight="C")
                + SearchVector("reference", weight="D")
            )
            hadith_qs = (
                Hadith.objects.select_related("chapter", "chapter__book")
                .annotate(rank=SearchRank(hadith_vector, search_query))
                .filter(rank__gt=0)
                .order_by("-rank")
            )

            azkar_vector = SearchVector("title", weight="A") + SearchVector(
                "arabic", weight="B"
            ) + SearchVector("urdu", weight="C")
            azkar_qs = (
                Azkar.objects.select_related("category")
                .annotate(rank=SearchRank(azkar_vector, search_query))
                .filter(rank__gt=0)
                .order_by("-rank")
            )

            research_vector = (
                SearchVector("title", weight="A")
                + SearchVector("summary", weight="B")
                + SearchVector("references", weight="C")
                + SearchVector("author", weight="D")
            )
            research_qs = (
                ResearchPaper.objects.annotate(rank=SearchRank(research_vector, search_query))
                .filter(rank__gt=0)
                .order_by("-rank")
            )

            combined = (
                [("quran", a, float(getattr(a, "rank", 0.0))) for a in ayah_qs[:50]]
                + [("hadith", h, float(getattr(h, "rank", 0.0))) for h in hadith_qs[:50]]
                + [("azkar", z, float(getattr(z, "rank", 0.0))) for z in azkar_qs[:50]]
                + [("research", r, float(getattr(r, "rank", 0.0))) for r in research_qs[:50]]
            )
            combined.sort(key=lambda x: x[2], reverse=True)
        else:
            ayah_qs = QuranAyah.objects.select_related("surah").filter(
                Q(text_ar__icontains=query)
                | Q(translation_ur__icontains=query)
                | Q(translation_en__icontains=query)
            )
            hadith_qs = Hadith.objects.select_related("chapter", "chapter__book").filter(
                Q(text_ar__icontains=query)
                | Q(text_ur__icontains=query)
                | Q(text_en__icontains=query)
                | Q(reference__icontains=query)
            )
            azkar_qs = Azkar.objects.select_related("category").filter(
                Q(title__icontains=query) | Q(arabic__icontains=query) | Q(urdu__icontains=query)
            )
            research_qs = ResearchPaper.objects.filter(
                Q(title__icontains=query)
                | Q(summary__icontains=query)
                | Q(references__icontains=query)
                | Q(author__icontains=query)
            )
            combined = (
                [("quran", a, 0.0) for a in ayah_qs[:50]]
                + [("hadith", h, 0.0) for h in hadith_qs[:50]]
                + [("azkar", z, 0.0) for z in azkar_qs[:50]]
                + [("research", r, 0.0) for r in research_qs[:50]]
            )

    paginator = Paginator(combined, 20)
    page_obj = paginator.get_page(page_number)

    context = {
        "query": query,
        "page_obj": page_obj,
        "counts": {
            "quran": ayah_qs.count() if query else 0,
            "hadith": hadith_qs.count() if query else 0,
            "azkar": azkar_qs.count() if query else 0,
            "research": research_qs.count() if query else 0,
        },
    }
    return render(request, "core/search.html", context)

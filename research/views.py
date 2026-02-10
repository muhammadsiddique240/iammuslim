from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import ResearchPaper


def paper_list(request: HttpRequest) -> HttpResponse:
    page_number = request.GET.get("page", "1")
    paginator = Paginator(ResearchPaper.objects.all(), 12)
    page_obj = paginator.get_page(page_number)
    return render(request, "research/paper_list.html", {"page_obj": page_obj})


def paper_detail(request: HttpRequest, slug: str) -> HttpResponse:
    paper = get_object_or_404(ResearchPaper, slug=slug)
    return render(request, "research/paper_detail.html", {"paper": paper})

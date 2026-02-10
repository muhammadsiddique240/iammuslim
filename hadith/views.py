from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import HadithBook, HadithChapter


def book_list(request: HttpRequest) -> HttpResponse:
    books = HadithBook.objects.all()
    return render(request, "hadith/book_list.html", {"books": books})


def book_detail(request: HttpRequest, slug: str) -> HttpResponse:
    book = get_object_or_404(HadithBook, slug=slug)
    chapters = book.chapters.all()
    return render(request, "hadith/book_detail.html", {"book": book, "chapters": chapters})


def chapter_detail(request: HttpRequest, book_slug: str, chapter_slug: str) -> HttpResponse:
    book = get_object_or_404(HadithBook, slug=book_slug)
    chapter = get_object_or_404(HadithChapter, book=book, slug=chapter_slug)
    page_number = request.GET.get("page", "1")
    paginator = Paginator(chapter.hadiths.all(), 20)
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "hadith/chapter_detail.html",
        {"book": book, "chapter": chapter, "page_obj": page_obj},
    )

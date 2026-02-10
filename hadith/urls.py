from django.urls import path

from . import views

app_name = "hadith"

urlpatterns = [
    path("", views.book_list, name="book_list"),
    path("<slug:slug>/", views.book_detail, name="book_detail"),
    path("<slug:book_slug>/<slug:chapter_slug>/", views.chapter_detail, name="chapter_detail"),
]

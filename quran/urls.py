from django.urls import path

from . import views

app_name = "quran"

urlpatterns = [
    path("", views.surah_list, name="surah_list"),
    path("<slug:slug>/", views.surah_detail, name="surah_detail"),

    # JSON API endpoints
    path("api/ar/", views.quran_arabic_json, name="quran_arabic_json"),
    path("api/ur/", views.quran_urdu_json, name="quran_urdu_json"),
    path("api/ar/surah/<int:surah_number>/", views.quran_surah_json, name="quran_surah_json"),
    path("api/ur/surah/<int:surah_number>/", views.quran_surah_urdu_json, name="quran_surah_urdu_json"),
    path("api/info/", views.quran_info_json, name="quran_info_json"),
]

from django.urls import path

from . import views

app_name = "azkar"

urlpatterns = [
    path("", views.category_list, name="category_list"),
    path("morning/", views.morning, name="morning"),
    path("evening/", views.evening, name="evening"),
    path("<slug:slug>/", views.category_detail, name="category_detail"),
]

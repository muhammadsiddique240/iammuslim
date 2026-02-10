from django.urls import path

from . import views

app_name = "research"

urlpatterns = [
    path("", views.paper_list, name="paper_list"),
    path("<slug:slug>/", views.paper_detail, name="paper_detail"),
]

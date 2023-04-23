from django.urls import path
from .views import quran_home, sura_details

urlpatterns = [
    path("home", quran_home, name="quran-home"),
    path("sura/<int:id>", sura_details, name="sura-details"),
]
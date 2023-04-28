from django.urls import path
from .views import quran_home, sura_details, sura_translate, sura_tafseer, sura_reading, verses

urlpatterns = [
    path("home", quran_home, name="quran-home"),
    path("sura/<int:id>", sura_details, name="sura-details"),
    path("sura/<int:id>/verse", verses, name="verses"),
    path("sura/<int:id>/translate", sura_translate, name="sura_translate"),
    path("sura/<int:id>/tafseer", sura_tafseer, name="sura_tafseer"),
    path("sura/<int:id>/read", sura_reading, name="sura_read"),
]
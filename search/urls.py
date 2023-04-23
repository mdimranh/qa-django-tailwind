from django.urls import path
from .views import search_quran
from .qsearch import search_question

urlpatterns = [
    path("search/quran", search_quran, name="quranSearch"),
    path("search/question", search_question, name="questionSearch")
]

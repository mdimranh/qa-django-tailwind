from django.shortcuts import render
from django.views import View
from question.models import Question


class Home(View):
    def get(self, request):
        questions = Question.objects.all().order_by("created_at")
        context = {'questions': questions}
        return render(request, "home.html", context)

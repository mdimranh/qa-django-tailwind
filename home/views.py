from django.shortcuts import render
from django.views import View


class Home(View):
    def get(self, request):
        questions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        context = {'questions': questions}
        return render(request, "home.html", context)

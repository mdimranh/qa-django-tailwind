from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.shortcuts import redirect, render
from django.views import View


class Login(View):
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        # remember = request.POST.get('remember_me', False)
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)
            # if not remember:
            #     request.session.set_expiry(0)
            return redirect('/')
        else:
            messages.info(request, 'Invalid username or password!')
            return redirect('login')

class Registration(View):
    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User(first_name=first_name, last_name=last_name, email=email, username=email)
        user.set_password(password)
        user.save(self)
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid username or password!')
            return redirect('login')

def logout(request):
    auth.logout(request)
    return redirect('/')
from django.urls import path

from .views import *

urlpatterns = [
    path('login', Login.as_view(), name='login'),
    path('join', Registration.as_view(), name='login'),
    path('logout', logout, name='logout')
]
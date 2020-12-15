from django.urls import path

from .views import *

urlpatterns = [
    path('', home),
    path('oauth/', oauth),
    path('events/', events),
    path('logout/', logout)
]

from django.urls import path

from . import views
from .views import register

urlpatterns = [
    path('', views.register),
    path('verify', views.verificate_me, name="verifysecondstage"),

]
from django.contrib import admin
from django.urls import path
from .views import compileScribblet, interpretScribblet

urlpatterns = [
    path("compile", compileScribblet),
    path("interpret", interpretScribblet),
]
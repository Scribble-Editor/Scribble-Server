from django.urls import path
from .views import create, delete, insert, remove, find, listAll, changeSecret

urlpatterns = [
  path('create', create),
  path('delete', delete),
  path('insert', insert),
  path('remove', remove),
  path('find', find),
  path('all', listAll),
  path('change-secret', changeSecret)
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Example path for the index view
]

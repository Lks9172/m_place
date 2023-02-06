
from django.urls import path
from .views import generate_trearment

urlpatterns = [
    path("", generate_trearment),
]

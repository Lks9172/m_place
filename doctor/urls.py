
from django.urls import path
from .views import search_doctor

urlpatterns = [
    path("", search_doctor),
]

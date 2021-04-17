from django.urls import path, include
from Spider import views

urlpatterns = [
    path('', views.getCourse)
]

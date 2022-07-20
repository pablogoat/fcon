from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name="home"),
    path('create/', views.create, name="create"),
    path('sheets/', views.allsheets, name="sheets"),
]

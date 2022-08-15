from unicodedata import name
from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name="home"), #home page
    path('create/', views.create, name="create"), #create new reckoning page
    path('sheets/', views.allsheets, name="sheets"), #list of all reckonings
    path('reckon/<str:name>', views.reckon, name="reckon"), #given reckoning page
    path('reckon/<str:name>/<str:new_item>', views.debet, name="debet"), #input debtors for the given item
    path('<str:name>/transactions', views.transactions, name="transactions") #show calculated transactions
]

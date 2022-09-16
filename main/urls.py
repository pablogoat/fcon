from unicodedata import name
from . import views
from django.urls import path

urlpatterns = [
    # home page
    path('', views.home, name="home"),
    # create new reckoning page
    path('create/', views.create, name="create"),
    # list of all reckonings
    path('sheets/', views.allsheets, name="sheets"),
    # given reckoning page
    path('reckon/<str:name>', views.reckon, name="reckon"),
    # input debtors for the given item
    path('reckon/<str:name>/<str:new_item>', views.debet, name="debet"),
    # show calculated transactions
    path('<str:name>/transactions', views.transactions, name="transactions")
]

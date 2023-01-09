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
    path('reckon/<int:sheetid>', views.reckon, name="reckon"),
    # input debtors for the given item
    path('reckon/<int:sheetid>/<str:new_item>', views.debet, name="debet"),
    # show calculated transactions
    path('<int:sheetid>/transactions', views.transactions, name="transactions")
]

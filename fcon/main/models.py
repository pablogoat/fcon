from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Sheet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sheet", null=True)
    name = models.CharField(max_length=30)
    unapproved_item = models.CharField(max_length=30 ,default='')

    def __str__(self):
        return self.name

class Person(models.Model):
    sheet = models.ForeignKey(Sheet, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    balance = models.FloatField(default=0)

    def __str__(self):
        return self.name

class Item(models.Model):
    sheet = models.ForeignKey(Sheet, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    value = models.FloatField()

    def __str__(self):
        return self.name

class Debtor(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    share = models.FloatField(null=True)

    def __str__(self):
        return self.person.name

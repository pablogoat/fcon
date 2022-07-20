from django import forms

class sheetCreator(forms.Form):
    name = forms.CharField(label="Name", max_length=30)
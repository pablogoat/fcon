from django import forms
from main.models import Person, Sheet, Item, Debtor

class sheetCreator(forms.Form):
    name = forms.CharField(label="Name", max_length=30)

class addPerson(forms.Form):
    name = forms.CharField(label="Name", max_length=30)

class addItem(forms.Form):
    item = forms.CharField(label="item", max_length=30)
    value = forms.FloatField(label="value")
    
    """def __init__(self):
        super(addItem, self).__init__()
        people = [i.name for i in Person.objects.all()]

        self.fields["pay"]  = forms.ChoiceField(
            widget=forms.Select(choices=people),
        )
    """
from unicodedata import name
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect

from main.models import Person, Sheet, Item, Debetor
from .forms import sheetCreator

# Create your views here.

def home(response):

    return render(response, "main/home.html", {})

def create(response):
    if response.method == 'POST':
        print(response.POST)
        form = sheetCreator(response.POST)

        if form.is_valid():
            t = Sheet(name=form.cleaned_data["name"])
            t.save()

        return HttpResponseRedirect('/', {})
    else:
        form = sheetCreator()

        return render(response, "main/create.html", {"form": form})

def allsheets(response):

    if response.method == 'POST':
        print(response.POST)

        return HttpResponseRedirect('/reckon/%s' %response.POST.get("edit"))

    else:
        t = Sheet.objects.all()

        return render(response, "main/sheets.html", {"sheets": t})

def reckon(response, name):

    if response.method == 'POST':
        if response.POST.get("delete"):
            view = Sheet.objects.get(name=response.POST.get("delete"))
            view.delete()

            return HttpResponseRedirect('/sheets/', {})
        elif response.POST.get("addperson"):
            view = Sheet.objects.get(name=response.POST.get("addperson"))
            
            if response.POST.get("data"):
                person = Person(sheet=view, name=response.POST.get("data"))
                print(person)
                person.save()

            return HttpResponseRedirect('/sheets/', {})
        elif response.POST.get("additem"):
            view = Sheet.objects.get(name=response.POST.get("additem"))

            postItem = response.POST.get("item")
            postPay = response.POST.get("pay")
            postValue = float("{:.2f}".format(float(response.POST.get("value"))))

            if postItem and postPay and postValue:                
                if Person.objects.filter(sheet=view, name=postPay).exists():
                    new_item = Item(sheet=view, person=Person.objects.get(sheet=view, name=postPay), name=postItem, value=postValue)
                    print(new_item)
                    test = Person.objects.get(sheet=view, name=postPay)
                    test.balance -= postValue
                    test.save()
                    new_item.save()
                else:
                    newPerson = Person(sheet=view, name=postPay, balance=-postValue)
                    print(newPerson)
                    newPerson.save()

                    new_item = Item(sheet=view, person=newPerson, name=postItem, value=postValue)
                    print(new_item)
                    new_item.save()

            return HttpResponseRedirect('/reckon/{}/{}'.format(view.name, postItem))
        else:
            return HttpResponseRedirect('/', {})

    else:
        view = Sheet.objects.get(name=name)
        print(view)
        people = [i for i in Person.objects.filter(sheet=view)]
        items = [i for i in Item.objects.filter(sheet=view)]

        return render(response, "main/reckon.html", {"view": view, "people": people, "items": items})

def debet(response, name, new_item): #function for spliting expense among people

    view = Sheet.objects.get(name=name)

    if response.method == 'POST':
        sum_share = 100
        count = 0

        for person in Person.objects.filter(sheet=view):
            if response.POST.get(person.name) == 'clicked':
                count += 1
                if response.POST.get('d' + person.name) != '':
                    sum_share -= float("{:.2f}".format(float(response.POST.get('d' + person.name))))
                    count -= 1
            print(count)
                

        for p in Person.objects.filter(sheet=view):
            if response.POST.get(p.name) == 'clicked':
                if response.POST.get('d' + p.name) != '':
                    new_debetor = Debetor(person=p, item=Item.objects.get(sheet=view, name=new_item), share=float("{:.2f}".format(float(response.POST.get('d' + p.name)))))
                else:
                    print(count)
                    new_debetor = Debetor(person=p, item=Item.objects.get(sheet=view, name=new_item), share=sum_share/count)
                    sum_share -= new_debetor.share
                    count -= 1
                new_debetor.save()
                print(str(new_debetor.item) + " " + new_debetor.person.name + " " + str(new_debetor.share))
        
        return HttpResponseRedirect('/sheets/', {})

    
    else:
        debt = [i for i in Person.objects.filter(sheet=view)]

        return render(response, "main/debet.html", {"debt": debt, "view": view, "item": Item.objects.get(sheet=view, name=new_item)})

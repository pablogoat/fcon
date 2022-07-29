from ctypes import sizeof
from unicodedata import name
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect

from main.models import Person, Sheet, Item, Debtor
from .forms import sheetCreator
from main.transaction import transaction

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
        elif response.POST.get("show"):
            view = Sheet.objects.get(name=response.POST.get("show"))
            
            return HttpResponseRedirect('/{}/transactions'.format(view.name))
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
                    new_Debtor = Debtor(person=p, item=Item.objects.get(sheet=view, name=new_item), share=float("{:.2f}".format(float(response.POST.get('d' + p.name)))))
                else:
                    print(count)
                    new_Debtor = Debtor(person=p, item=Item.objects.get(sheet=view, name=new_item), share=sum_share/count)
                    sum_share -= new_Debtor.share
                    count -= 1
                new_Debtor.person.balance += new_Debtor.item.value * new_Debtor.share/100
                new_Debtor.person.save()
                new_Debtor.save()
                print(str(new_Debtor.item) + " " + new_Debtor.person.name + " " + str(new_Debtor.share))
        
        return HttpResponseRedirect('/sheets/', {})

    
    else:
        debt = [i for i in Person.objects.filter(sheet=view)]

        return render(response, "main/debet.html", {"debt": debt, "view": view, "item": Item.objects.get(sheet=view, name=new_item)})

def transactions(response, name): #function that shows transactions needed to complete the reckoning
    view = Sheet.objects.get(name=name)
    debtors = [person for person in Person.objects.filter(sheet=view) if person.balance > 0]
    collectors = [person for person in Person.objects.filter(sheet=view) if person.balance < 0]

    debtors.sort(reverse=True, key=PersonCmp)
    collectors.sort(reverse=True, key=PersonCmp)

    print(debtors)
    print(collectors)

    actions = []

    while len(debtors) and len(collectors):
        if debtors[0].balance < collectors[0].balance * -1:
            actions.append(transaction(debtors[0].name,str(debtors[0].balance),collectors[0].name))
            collectors[0].balance += debtors[0].balance
            debtors.pop(0)
        elif debtors[0].balance == collectors[0].balance * -1:
            actions.append(transaction(debtors[0].name,str(debtors[0].balance),collectors[0].name))
            collectors.pop(0)
            debtors.pop(0)
        else:
            actions.append(transaction(debtors[0].name,str(collectors[0].balance * -1),collectors[0].name))
            debtors[0].balance += collectors[0].balance
            collectors.pop(0)

    print(actions)

    return render(response, 'main/transactions.html', {"actions": actions})

def PersonCmp(p1):
    
    return p1.balance
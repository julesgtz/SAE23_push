from django.shortcuts import render, redirect
from .forms import ServicesForms
from django.http import HttpResponseRedirect

from . import models

def ajout(request):
    form = ServicesForms
    return render(request, "adminsite/services/ajout.html", {"form": form})
def traitement(request):
    form = ServicesForms(request.POST)
    if form.is_valid():
        app = form.save()
        return HttpResponseRedirect("/adminsite/services/")
    else:
        return render(request, "adminsite/services/ajout.html", {"form": form})

def index(request):
    app = list(models.Services.objects.all())
    return render(request, 'adminsite/services/affiche.html',{"liste": app})

def delete(request, id):
    stream = models.Services.objects.get(pk=id)
    stream.delete()
    return HttpResponseRedirect("/adminsite/services/")

def update_traitement(request, id):
    mform = ServicesForms(request.POST)
    if mform.is_valid():
        mag = mform.save(commit=False)
        mag.id = id
        mag.save()
        return HttpResponseRedirect("/adminsite/services/")
    else:
        return render(request, "adminsite/services/update_affiche.html", {"form": mform, "id": id})

def update(request, id):
    serv = models.Services.objects.get(pk=id)
    form = ServicesForms(serv.dico())
    return render(request,"adminsite/services/update.html",{"form":form, "id": id})

def affiche(request, id):
    var = models.Services.objects.get(pk=id)
    return render(request,"adminsite/services/affiche.html",{"util": var, "id": id})

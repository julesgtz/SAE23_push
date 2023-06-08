from django.shortcuts import render, redirect
from .forms import FichesForms
from . import models
from django.http import HttpResponseRedirect


def ajout(request):
    form = FichesForms
    return render(request, "adminsite/fiches/ajout.html", {"form": form})
def traitement(request):
    form = FichesForms(request.POST)
    if form.is_valid():
        app = form.save()
        return HttpResponseRedirect("/adminsite/fiches/")
    else:
        return render(request, "adminsite/fiches/ajout.html", {"form": form})

def index(request):
    app = list(models.Fiches.objects.all())
    return render(request, 'adminsite/fiches/affiche.html',{"liste": app})

def delete(request, id):
    stream = models.Fiches.objects.get(pk=id)
    stream.delete()
    return HttpResponseRedirect("/adminsite/fiches/")

def update_traitement(request, id):
    mform = FichesForms(request.POST)
    if mform.is_valid():
        mag = mform.save(commit=False)
        mag.id = id
        mag.save()
        return HttpResponseRedirect("/adminsite/fiches/")
    else:
        return render(request, "adminsite/fiches/update_affiche.html", {"form": mform, "id": id})

def update(request, id):
    f = models.Fiches.objects.get(pk=id)
    form = FichesForms(f.dico())
    return render(request,"adminsite/fiches/ajout.html",{"form":form, "id": id})

def affiche(request, id):
    var = models.Fiches.objects.get(pk=id)
    return render(request,"adminsite/fiches/affiche.html",{"util": var, "id": id})
from django.shortcuts import render, redirect
from .forms import ApplicationsForms
from django.http import HttpResponseRedirect
from . import models

def ajout(request):
    form = ApplicationsForms
    return render(request, "adminsite/applications/ajout.html", {"form": form})
def traitement(request):
    form = ApplicationsForms(request.POST)
    if form.is_valid():
        app = form.save()
        return HttpResponseRedirect("/adminsite/applications/")
    else:
        return render(request, "adminsite/applications/ajout.html", {"form": form})

def index(request):
    app = list(models.Applications.objects.all())
    return render(request, 'adminsite/applications/affiche.html',{"liste": app})

def delete(request, id):
    stream = models.Applications.objects.get(pk=id)
    stream.delete()
    return HttpResponseRedirect("/adminsite/applications/")

def update_traitement(request, id):
    mform = ApplicationsForms(request.POST)
    if mform.is_valid():
        mag = mform.save(commit=False)
        mag.id = id
        mag.save()
        return HttpResponseRedirect("/adminsite/applications/")
    else:
        return render(request, "adminsite/applications/update_affiche.html", {"form": mform, "id": id})

def update(request, id):
    a = models.Applications.objects.get(pk=id)
    form = ApplicationsForms(a.dico())
    return render(request,"adminsite/applications/ajout.html",{"form":form, "id": id})

def affiche(request, id):
    var = models.Fiches.objects.get(pk=id)
    return render(request,"adminsite/applications/affiche.html",{"util": var, "id": id})
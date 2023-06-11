from django.shortcuts import render, redirect
from .forms import ServeursForms
from . import models
from django.http import HttpResponseRedirect

def ajout(request):
    form = ServeursForms
    return render(request, "adminsite/serveurs/ajout.html", {"form": form})
def traitement(request):
    form = ServeursForms(request.POST)
    if form.is_valid():
        app = form.save()
        return HttpResponseRedirect("/adminsite/serveurs/")
    else:
        return render(request, "adminsite/serveurs/ajout.html", {"form": form})

def index(request):
    app = list(models.Serveurs.objects.all())
    return render(request, 'adminsite/serveurs/affiche.html',{"liste": app})

def delete(request, id):
    stream = models.Serveurs.objects.get(pk=id)
    stream.delete()
    return HttpResponseRedirect("/adminsite/serveurs/")

def update_traitement(request, id):
    mform = ServeursForms(request.POST)
    if mform.is_valid():
        mag = mform.save(commit=False)
        mag.id = id
        mag.save()
        return HttpResponseRedirect("/adminsite/serveurs/")
    else:
        return render(request, "adminsite/serveurs/update_affiche.html", {"form": mform, "id": id})

def update(request, id):
    serv = models.Serveurs.objects.get(pk=id)
    form = ServeursForms(serv.dico())
    return render(request,"adminsite/serveurs/update.html",{"form":form, "id": id})

def affiche(request, id):
    var = models.Serveurs.objects.get(pk=id)
    return render(request,"adminsite/serveurs/affiche.html",{"util": var, "id": id})

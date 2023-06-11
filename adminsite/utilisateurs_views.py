from django.shortcuts import render, redirect
from .forms import UtilisateursForms
from . import models
from django.http import HttpResponseRedirect

def ajout(request):
    form = UtilisateursForms
    return render(request, "adminsite/utilisateurs/ajout.html", {"form": form})
def traitement(request):
    form = UtilisateursForms(request.POST)
    if form.is_valid():
        app = form.save()
        return HttpResponseRedirect("/adminsite/utilisateurs/")

    else:
        return render(request, "adminsite/utilisateurs/ajout.html", {"form": form})

def index(request):
    app = list(models.Utilisateurs.objects.all())
    return render(request, 'adminsite/utilisateurs/affiche.html',{"liste": app})

def delete(request, id):
    stream = models.Utilisateurs.objects.get(pk=id)
    stream.delete()
    return HttpResponseRedirect("/adminsite/utilisateurs/")


def update_traitement(request, id):
    mform = UtilisateursForms(request.POST)
    if mform.is_valid():
        mag = mform.save(commit=False)
        mag.id = id
        mag.save()
        return HttpResponseRedirect("/adminsite/utilisateurs/")
    else:
        return render(request, "adminsite/utilisateurs/update_affiche.html", {"form": mform, "id": id})

def update(request, id):
    util = models.Utilisateurs.objects.get(pk=id)
    form = UtilisateursForms(util.dico())
    return render(request,"adminsite/utilisateurs/update.html",{"form":form, "id": id})

def affiche(request, id):
    var = models.Utilisateurs.objects.get(pk=id)
    return render(request,"adminsite/utilisateurs/affiche.html",{"util": var, "id": id})

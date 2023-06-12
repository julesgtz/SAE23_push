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
        donnees = form.save(commit=False)
        stockage = donnees.stockage_use
        vive = donnees.memoire_vive
        serveur = models.Serveurs.objects.get(pk=donnees.serveur_lancement.id)
        stockage_serveur = serveur.stockage
        memoire_serveur = serveur.memoire
        if serveur.stockage.endswith("Go"):
            serveur.stockage = int(serveur.stockage[:-2]) * 1_000
        elif serveur.stockage.endswith("To"):
            serveur.stockage = int(serveur.stockage[:-2]) * 1_000_000

        donnees.stockage_use = int(donnees.stockage_use)
        serveur.stockage = int(serveur.stockage)

        if donnees.stockage_use>serveur.stockage:
            "erreur pas assez de stockage"
        else:
            donnees.stockage_use = serveur.stockage - donnees.stockage_use
            donnees.stockage_use = str(donnees.stockage_use)
            print(donnees.serveur_lancement.id)
            serveur_update = models.Serveurs.objects.get(id=donnees.serveur_lancement.id)
            serveur_update.stockage = donnees.stockage_use
            serveur_update.save()

        app = form.save()
        return HttpResponseRedirect("/adminsite/services/")
    else:
        return render(request, "adminsite/services/ajout.html", {"form": form})

def index(request):
    app = list(models.Services.objects.all())
    return render(request, 'adminsite/services/affiche.html',{"liste": app})

def delete(request, id):

    # quand on supprime un services, rajouter au serveur l'espace qu'il utilisait
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

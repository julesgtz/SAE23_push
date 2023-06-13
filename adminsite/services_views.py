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

        donnees.memoire_vive = str(donnees.memoire_vive)
        if donnees.memoire_vive.endswith("Go"):
            donnees.memoire_vive = float(donnees.memoire_vive[:-2]) * 1_000

        elif donnees.memoire_vive.endswith("To"):
            donnees.memoire_vive = float(donnees.memoire_vive[:-2]) * 1_000_000

        donnees.memoire_vive = float(donnees.memoire_vive)
        donnees.memoire_vive = int(donnees.memoire_vive) * 1000


        if donnees.memoire_vive <= 1_000_000:
            donnees.memoire_vive = donnees.memoire_vive / 1000
            donnees.memoire_vive = int(donnees.memoire_vive)
            donnees.memoire_vive = str(donnees.memoire_vive) + "Go"
        else:
            donnees.memoire_vive = donnees.memoire_vive / 1_000_000
            donnees.memoire_vive = int(donnees.memoire_vive)
            donnees.memoire_vive = str(donnees.memoire_vive) + "To"

        serveur = models.Serveurs.objects.get(pk=donnees.serveur_lancement.id)
        donnees.stockage_use = int(donnees.stockage_use) * 1000
        serveur.stockage = str(serveur.stockage)
        if serveur.stockage.endswith("Go"):
            serveur.stockage = float(serveur.stockage[:-2]) * 1_000

        elif serveur.stockage.endswith("To"):
            serveur.stockage = float(serveur.stockage[:-2]) * 1_000_000

        donnees.stockage_use = float(donnees.stockage_use)
        serveur.stockage = float(serveur.stockage)

        if donnees.stockage_use>serveur.stockage:
            return render(request, "adminsite/services/ajout.html", {"form": form, "error": "Erreur pas assez de stockage sur le serveur"})
        else:
            donnees.stockage_use = serveur.stockage - donnees.stockage_use
            serveur_update = models.Serveurs.objects.get(id=donnees.serveur_lancement.id)

            if donnees.stockage_use <= 1_000_000:
                serveur_update.stockage =  donnees.stockage_use / 1000
                serveur_update.stockage = int(serveur_update.stockage)
                serveur_update.stockage = str(serveur_update.stockage)+"Go"
            else:
                serveur_update.stockage = donnees.stockage_use / 1_000_000
                serveur_update.stockage = int(serveur_update.stockage)
                serveur_update.stockage = str(serveur_update.stockage) + "To"

            serveur_update.save()

            stockage = float(stockage)
            if stockage < 1_000:
                stockage = int(stockage)
                stockage = str(stockage) + "Go"
            else:
                stockage = int(stockage)
                stockage = str(stockage) + "To"

            donnees.stockage_use = stockage
            app = form.save()
        return HttpResponseRedirect("/adminsite/services/")
    else:
        return render(request, "adminsite/services/ajout.html", {"form": form})

def index(request):
    app = list(models.Services.objects.all())
    return render(request, 'adminsite/services/affiche.html',{"liste": app})

def delete(request, id):
    donnees = models.Services.objects.get(pk=id)
    serveur = models.Serveurs.objects.get(pk=donnees.serveur_lancement.id)

    donnees.stockage_use = str(donnees.stockage_use)
    if donnees.stockage_use.endswith("Go"):
        donnees.stockage_use = float(donnees.stockage_use[:-2]) * 1_000

    elif donnees.memoire_vive.endswith("To"):
        donnees.stockage_use = float(donnees.stockage_use[:-2]) * 1_000_000

    serveur.stockage = str(serveur.stockage)
    if serveur.stockage.endswith("Go"):
        serveur.stockage = float(serveur.stockage[:-2]) * 1_000

    elif serveur.stockage.endswith("To"):
        serveur.stockage = float(serveur.stockage[:-2]) * 1_000_000

    donnees.stockage_use = float(donnees.stockage_use)
    serveur.stockage = float(serveur.stockage)

    serveur.stockage = serveur.stockage + donnees.stockage_use

    if serveur.stockage < 1_000_000:
        serveur.stockage = serveur.stockage / 1000
        serveur.stockage = int(serveur.stockage)
        serveur.stockage = str(serveur.stockage) + "Go"
    else:
        serveur.stockage = serveur.stockage / 1_000_000
        serveur.stockage = int(serveur.stockage)
        serveur.stockage = str(serveur.stockage) + "To"

    serveur.save()

    donnees.delete()

    return HttpResponseRedirect("/adminsite/services/")

def update_traitement(request, id):
    mform = ServicesForms(request.POST)

    service = models.Services.objects.get(pk=id)

    if mform.is_valid():
        donnees = mform.save(commit=False)

        stockage = donnees.stockage_use

        if service.stockage_use.endswith("Go"):
            service.stockage_use = float(service.stockage_use[:-2]) * 1_000

        elif service.stockage_use.endswith("To"):
            service.stockage_use = float(service.stockage_use[:-2]) * 1_000_000

        if donnees.stockage_use.endswith("Go"):
            donnees.stockage_use = float(donnees.stockage_use[:-2]) * 1_000
            stockage = donnees.stockage_use

        elif donnees.stockage_use.endswith("To"):
            donnees.stockage_use = float(donnees.stockage_use[:-2]) * 1_000_000
            stockage = donnees.stockage_use

        serveur = models.Serveurs.objects.get(pk=donnees.serveur_lancement.id)

        if service.stockage_use > donnees.stockage_use:
            donnees.stockage_use = service.stockage_use - donnees.stockage_use
            if serveur.stockage.endswith("Go"):
                serveur.stockage = float(serveur.stockage[:-2]) * 1_000

            elif serveur.stockage.endswith("To"):
                serveur.stockage = float(serveur.stockage[:-2]) * 1_000_000
            serveur.stockage = serveur.stockage + donnees.stockage_use

        else:
            donnees.stockage_use = donnees.stockage_use - service.stockage_use
            if serveur.stockage.endswith("Go"):
                serveur.stockage = float(serveur.stockage[:-2]) * 1_000

            elif serveur.stockage.endswith("To"):
                serveur.stockage = float(serveur.stockage[:-2]) * 1_000_000

            serveur.stockage = serveur.stockage - donnees.stockage_use

        if serveur.stockage<0:
                return render(request, "adminsite/services/update.html", {"form": mform, "error": "Erreur pas assez de stockage sur le serveur", "id": id})
        else:
            if serveur.stockage < 1_000_000:
                serveur.stockage = serveur.stockage / 1000
                serveur.stockage = int(serveur.stockage)
                serveur.stockage = str(serveur.stockage) + "Go"
            else:
                serveur.stockage = serveur.stockage / 1_000_000
                serveur.stockage = int(serveur.stockage)
                serveur.stockage = str(serveur.stockage) + "To"

            serveur.save()

            stockage = float(stockage)
            if stockage < 1_000_000:
                stockage = int(stockage)
                stockage = str(stockage / 1_000) + "Go"
            else:
                stockage = int(stockage)
                stockage = str(stockage / 1_000_000) + "To"

            donnees.stockage_use = stockage
            donnees.id = id
            donnees.save()



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

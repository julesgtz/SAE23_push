from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import ServicesForms
from .models import Services
from . import models
import requests
import os


# Create your views here.
def index(request):
    return render(request, 'adminsite/index.html')


def importe(request):
    if request.method=="POST" and request.FILES['fichier']:
        fichier_texte = request.FILES['fichier']
        lignes = fichier_texte.readlines()
        for ligne in lignes:
            l = ligne.decode("utf-8")
            tasks = l.strip().split(',')
            if tasks[0] == "services":
                if len(tasks) != 6 :
                    resp = f"il manque {6-len(tasks)} champ(s) dans services"
                    return render(request, f'adminsite/import.html', {"succes": resp})
                else:
                    models.Services.objects.create(nom=tasks[1], date=tasks[2],stockage_use=tasks[3], memoire_vive=tasks[4], serveur_lancement_id=tasks[5])
                    return HttpResponseRedirect('/adminsite/services/')

            elif tasks[0] == "application":
                if len(tasks) != 4:
                    resp = f"il manque {4 - len(tasks)} champ(s) dans application"
                    return render(request, f'adminsite/import.html', {"succes": resp})
                else:
                    models.Applications.objects.create(nom=tasks[1], serveur_id=tasks[2], logo='images/applications_default.jpg',utilisateurs_id=tasks[3])
                    return HttpResponseRedirect('/adminsite/applications/')

            else:
                return render(request, 'adminsite/import.html', {"succes" : "soit services soit application"})
    return render(request, 'adminsite/import.html')
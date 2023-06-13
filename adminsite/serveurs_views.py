from django.shortcuts import render, redirect
from .forms import ServeursForms
from . import models
from django.http import HttpResponseRedirect
from fpdf import FPDF
from django.http import FileResponse

def ajout(request):
    form = ServeursForms
    return render(request, "adminsite/serveurs/ajout.html", {"form": form})
def traitement(request):
    form = ServeursForms(request.POST)
    if form.is_valid():
        donnees = form.save(commit=False)
        donnees.stockage_initial = donnees.stockage
        donnees.save()
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
    serv = models.Serveurs.objects.get(pk=id)

    serv.stockage_initial = str(serv.stockage_initial)
    if serv.stockage_initial.endswith("Go"):
        serv.stockage_initial = float(serv.stockage_initial[:-2]) * 1_000

    elif serv.stockage_initial.endswith("To"):
        serv.stockage_initial = float(serv.stockage_initial[:-2]) * 1_000_000
    serv.stockage_initial= float(serv.stockage_initial)

    serv.stockage = str(serv.stockage)
    if serv.stockage.endswith("Go"):
        serv.stockage = float(serv.stockage[:-2]) * 1_000

    elif serv.stockage.endswith("To"):
        serv.stockage = float(serv.stockage[:-2]) * 1_000_000
    serv.stockage= float(serv.stockage)

    stockage_service = serv.stockage_initial - serv.stockage

    mform = ServeursForms(request.POST)
    if mform.is_valid():
        serveur = mform.save(commit=False)

        serveur.stockage = str(serveur.stockage)
        if serveur.stockage.endswith("Go"):
            serveur.stockage = float(serveur.stockage[:-2]) * 1_000

        elif serveur.stockage.endswith("To"):
            serveur.stockage = float(serveur.stockage[:-2]) * 1_000_000
        serveur.stockage = float(serveur.stockage)

        if serveur.stockage < stockage_service:
            return render(request, "adminsite/serveurs/update.html", {"form": mform, "error": "Erreur pas assez de stockage sur le serveur","id": id})
        else:
            serveur.stockage_initial = serveur.stockage
            serveur.stockage = serveur.stockage - stockage_service
            if serveur.stockage < 1_000_000:
                serveur.stockage = serveur.stockage / 1000
                serveur.stockage = int(serveur.stockage)
                serveur.stockage = str(serveur.stockage) + "Go"
            else:
                serveur.stockage = serveur.stockage / 1_000_000
                serveur.stockage = int(serveur.stockage)
                serveur.stockage = str(serveur.stockage) + "To"

            if serveur.stockage_initial < 1_000_000:
                serveur.stockage_initial = serveur.stockage_initial / 1000
                serveur.stockage_initial = int(serveur.stockage_initial)
                serveur.stockage_initial = str(serveur.stockage_initial) + "Go"
            else:
                serveur.stockage_initial = serveur.stockage_initial / 1_000_000
                serveur.stockage_initial = int(serveur.stockage_initial)
                serveur.stockage_initial = str(serveur.stockage_initial) + "To"
            serveur.id = id
            serveur.save()
        return HttpResponseRedirect("/adminsite/serveurs/")
    else:
        return render(request, "adminsite/serveurs/update_affiche.html", {"form": mform, "id": id})

def update(request, id):
    serv = models.Serveurs.objects.get(pk=id)
    x = serv.stockage_initial
    serv.stockage_initial = serv.stockage
    serv.stockage = x
    form = ServeursForms(serv.dico())
    return render(request,"adminsite/serveurs/update.html",{"form":form, "id": id})

def affiche(request, id):
    var = models.Serveurs.objects.get(pk=id)
    return render(request,"adminsite/serveurs/affiche.html",{"util": var, "id": id})


def serveur_pdf(request,id):
    serveur = models.Serveurs.objects.get(pk=id)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=20)
    pdf.set_text_color(0, 0, 255)
    pdf.cell(200, 10,  ln=1, align='C')
    pdf.cell(200, 10, txt="RAPPORT SUR LE SERVEUR : " + serveur.nom, ln=1, align='C')
    pdf.cell(200, 10,  ln=1, align='C')
    pdf.set_font("Arial", size=15)
    pdf.cell(200, 10, txt="* Le serveur " + serveur.nom + " est un serveur de type " + models.Types.objects.get(
        pk=serveur.type.id).type, ln=2, align='L')
    pdf.cell(200, 10, txt="* Espace stockage: " + str(serveur.stockage_initial), ln=4, align='L')
    pdf.cell(200, 10, txt="* Espace restant: " + str(serveur.stockage), ln=5, align='L')
    pdf.cell(200, 10, txt="* Memoire vive: " + str(serveur.memoire), ln=6, align='L')
    pdf.cell(200, 10, txt="* Processeur: " + str(serveur.processeur), ln=8, align='L')
    line = 9
    pdf.cell(200, 10,  ln=1, align='C')
    if len(list(models.Applications.objects.filter(serveur=serveur))) == 0:
        pdf.cell(200, 10, txt="Il n'y a aucune application sur ce serveur.", ln=line, align='L')
        line = line + 1
    else:
        pdf.cell(200, 10, txt="* Les applications sur ce serveur:", ln=line, align='L')
        line = line + 1
        for i in list(models.Applications.objects.filter(serveur=serveur)):
            pdf.cell(200, 10, txt='         - ' +i.nom, ln=line, align='L')
            line = line + 1
    pdf.cell(200, 10,  ln=1, align='C')
    if len(list(models.Services.objects.filter(serveur_lancement=serveur))) == 0:
        pdf.cell(200, 10, txt="Il n'y a aucun service sur ce serveur.", ln=line, align='L')
        line = line + 1
    else:
        pdf.cell(200, 10, txt="* Les services sur ce serveur:", ln=line, align='L')
        line = line + 1
        for i in list(models.Services.objects.filter(serveur_lancement=serveur)):
            pdf.cell(200, 10, txt='         -'+i.nom, ln=line, align='L')
            line = line + 1
    pdf.output("Serveur-" + str(id) + ".pdf")
    response = FileResponse(open("Serveur-" + str(id) + ".pdf", 'rb'))
    return response

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


def serveur_pdf(request,id):
    serveur = models.Serveurs.objects.get(pk=id)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=20)
    pdf.cell(200, 10, txt="RAPPORT SUR LE SERVEUR : ", ln=1, align='C')
    pdf.cell(200, 10, txt=serveur.nom, ln=1, align='C')
    pdf.set_font("Arial", size=15)
    pdf.cell(200, 10, txt="Le serveur " + serveur.nom + " est un serveur de type " + models.Types.objects.get(
        pk=serveur.type.id).type, ln=2, align='C')
    pdf.cell(200, 10, txt="Espace stockage: " + str(serveur.stockage), ln=4, align='C')
    pdf.cell(200, 10, txt="Espace restant: " + "Mo", ln=5, align='C')
    pdf.cell(200, 10, txt="Memoire vive: " + str(serveur.memoire), ln=6, align='C')
    pdf.cell(200, 10, txt="Memoire vive non occupée: " + "Mo", ln=7, align='C')
    pdf.cell(200, 10, txt="Processeur: " + str(serveur.processeur), ln=8, align='C')
    line = 9
    if len(list(models.Applications.objects.filter(serveur=serveur))) == 0:
        pdf.cell(200, 10, txt="Il n'y a aucune application sur ce serveur.", ln=line, align='C')
        line = line + 1
    else:
        pdf.cell(200, 10, txt="Les applications sur ce serveur:", ln=line, align='C')
        line = line + 1
        for i in list(models.Applications.objects.filter(serveur=serveur)):
            pdf.cell(200, 10, txt=i.nom, ln=line, align='C')
            line = line + 1
    if len(list(models.Services.objects.filter(serveur_lancement=serveur))) == 0:
        pdf.cell(200, 10, txt="Il n'y a aucun service sur ce serveur.", ln=line, align='C')
        line = line + 1
    else:
        pdf.cell(200, 10, txt="Les services sur ce serveur:", ln=line, align='C')
        line = line + 1
        for i in list(models.Services.objects.filter(serveur_lancement=serveur)):
            pdf.cell(200, 10, txt=i.nom, ln=line, align='C')
            line = line + 1
    pdf.output("Serveur-" + str(id) + ".pdf")
    response = FileResponse(open("Serveur-" + str(id) + ".pdf", 'rb'))
    return response

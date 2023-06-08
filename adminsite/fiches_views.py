from django.shortcuts import render, redirect
from .forms import FichesForms
from . import models
from django.http import HttpResponseRedirect
from fpdf import FPDF
from django.http import FileResponse


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


def serveur_pdf(request,id):
    serveur = models.Serveurs.objects.get(pk=id)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial",size=20)
    pdf.cell(200,10,txt="RAPPORT SUR LE SERVEUR : ",ln = 1, align = 'C')
    pdf.cell(200, 10, txt=serveur.nom, ln=1, align='C')
    pdf.set_font("Arial", size=15)
    pdf.cell(200,10, txt="Le serveur " + serveur.nom + " est un serveur de type " + models.Types.objects.get(pk=serveur.type_de_serveur_id).type,ln = 2, align = 'C')
    pdf.cell(200, 10, txt="Espace stockage: " + str(serveur.stockage) + "Mo", ln=4,align='C')
    pdf.cell(200, 10, txt="Espace restant: " + "Mo", ln=5,align='C')
    pdf.cell(200, 10, txt="Memoire vive: " + str(serveur.memoire) + "Mo", ln=6, align='C')
    pdf.cell(200, 10, txt="Memoire vive non occupée: " + "Mo",ln=7, align='C')
    pdf.cell(200, 10, txt="Nombre de processeurs: " + str(serveur.processeurs), ln=8, align='C')
    line = 9
    if len(list(models.Applications.objects.filter(serveurs=serveur))) == 0:
        pdf.cell(200, 10, txt="Il n'y a aucune application sur ce serveur.", ln=line, align='C')
        line = line + 1
    else:
        pdf.cell(200, 10, txt="Les applications sur ce serveur:", ln=line, align='C')
        line = line + 1
        for i in list(models.Applications.objects.filter(serveurs=serveur)):
            pdf.cell(200, 10, txt=i.nom_application, ln=line, align='C')
            line = line + 1
    if len(list(models.Services.objects.filter(serveur_de_lancement=serveur))) == 0:
        pdf.cell(200, 10, txt="Il n'y a aucun service sur ce serveur.", ln=line, align='C')
        line = line + 1
    else:
        pdf.cell(200, 10, txt="Les services sur ce serveur:", ln=line, align='C')
        line = line + 1
        for i in list(models.Services.objects.filter(serveur_de_lancement=serveur)):
            pdf.cell(200, 10, txt=i.nom_service, ln=line, align='C')
            line = line + 1
    pdf.output("Serveur-" + str(id) + ".pdf")
    response = FileResponse(open("Serveur-" + str(id) + ".pdf", 'rb'))
    return response

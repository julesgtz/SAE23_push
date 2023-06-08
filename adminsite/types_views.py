from django.shortcuts import render, redirect
from .forms import TypesForms
from django.http import HttpResponseRedirect

from . import models

def ajout(request):
    form = TypesForms
    return render(request, "adminsite/types/ajout.html", {"form": form})
def traitement(request):
    form = TypesForms(request.POST)
    if form.is_valid():
        app = form.save()
        return HttpResponseRedirect("/adminsite/types/")
    else:
        return render(request, "adminsite/types/ajout.html", {"form": form})

def index(request):
    app = list(models.Types.objects.all())
    return render(request, 'adminsite/types/affiche.html',{"liste": app})

def delete(request, id):
    stream = models.Types.objects.get(pk=id)
    stream.delete()
    return HttpResponseRedirect("/adminsite/types/")

def update_traitement(request, id):
    mform = TypesForms(request.POST)
    if mform.is_valid():
        mag = mform.save(commit=False)
        mag.id = id
        mag.save()
        return HttpResponseRedirect("/adminsite/types/")
    else:
        return render(request, "adminsite/types/update_affiche.html", {"form": mform, "id": id})

def update(request, id):
    typ = models.Types.objects.get(pk=id)
    form = TypesForms(typ.dico())
    return render(request,"adminsite/types/ajout.html",{"form":form, "id": id})

def affiche(request, id):
    var = models.Types.objects.get(pk=id)
    return render(request,"adminsite/types/affiche.html",{"util": var, "id": id})

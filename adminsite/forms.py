from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from . import models
from django import forms

class ServeursForms(ModelForm):
    class Meta:
        model = models.Serveurs
        fields = ('nom','type','processeur','memoire','stockage',)
        labels = {
            'nom': _('Nom'),
            'type':_('Type de Serveur'),
            'processeur': _('Nombre de Processeur'),
            'memoire': _('Capacité Mémoire'),
            'stockage': _('Capacité de Stockage'),
        }
class TypesForms(ModelForm):
    class Meta:
        model = models.Types
        fields = ('type','description',)
        labels = {
            'type': _('Type'),
            'description':_('Description'),
        }
class UtilisateursForms(ModelForm):
    class Meta:
        model = models.Utilisateurs
        fields = ('nom','prenom','email',)
        labels = {
            'nom': _('Nom'),
            'prenom':_('Prenom'),
            'email': _('Email'),
        }
class ServicesForms(ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={"type" : "date"}))
    class Meta:
        model = models.Services
        fields = ('nom','date','stockage_use','memoire_vive','serveur_lancement')
        labels = {
            'nom': _('Nom du service'),
            'date':_('Date de lancement'),
            'stockage_use': _('Espace de stockage utilisé en Mbit'),
            'memoire_vive': _('Espace mémoire utilisé en Mbit'),
            'serveur_lancement': _('Serveur de lancement'),

        }
class ApplicationsForms(ModelForm):
    class Meta:
        model = models.Applications
        fields = ('nom','logo','serveur','utilisateurs',)
        labels = {
            'nom': _('Nom'),
            'logo':_('Logo'),
            'serveur': _('Serveur'),
            'utilisateurs': _('Utlisateur'),
        }

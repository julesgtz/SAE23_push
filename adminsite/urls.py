from django.urls import path
from . import views, serveurs_views, types_views, utilisateurs_views, services_views, applications_views, fiches_views


urlpatterns = [
    path('', views.index),

    path('serveurs/', serveurs_views.index),
    path('serveurs/update/<int:id>/', serveurs_views.update),
    path('serveurs/affiche/<int:id>/', serveurs_views.affiche),
    path('serveurs/traitement/', serveurs_views.traitement),
    path('serveurs/ajout/', serveurs_views.ajout),
    path('serveurs/delete/<int:id>/', serveurs_views.delete),
    path('serveurs/update_traitement/<int:id>/', serveurs_views.update_traitement),

    path('types/', types_views.index),
    path('types/update/<int:id>/', types_views.update),
    path('types/affiche/<int:id>/', types_views.affiche),
    path('types/traitement/', types_views.traitement),
    path('types/ajout/', types_views.ajout),
    path('types/delete/<int:id>/', types_views.delete),
    path('types/update_traitement/<int:id>/', types_views.update_traitement),

    path('utilisateurs/', utilisateurs_views.index),
    path('utilisateurs/update/<int:id>/', utilisateurs_views.update),
    path('utilisateurs/affiche/<int:id>/', utilisateurs_views.affiche),
    path('utilisateurs/traitement/', utilisateurs_views.traitement),
    path('utilisateurs/ajout/', utilisateurs_views.ajout),
    path('utilisateurs/delete/<int:id>/', utilisateurs_views.delete),
    path('utilisateurs/update_traitement/<int:id>/', utilisateurs_views.update_traitement),

    path('services/', services_views.index),
    path('services/update/<int:id>/', services_views.update),
    path('services/affiche/<int:id>/', services_views.affiche),
    path('services/traitement/', services_views.traitement),
    path('services/ajout/', services_views.ajout),
    path('services/delete/<int:id>/', services_views.delete),
    path('services/update_traitement/<int:id>/', services_views.update_traitement),

    path('applications/', applications_views.index),
    path('applications/update/<int:id>/', applications_views.update),
    path('applications/affiche/<int:id>/', applications_views.affiche),
    path('applications/traitement/', applications_views.traitement),
    path('applications/ajout/', applications_views.ajout),
    path('applications/delete/<int:id>/', applications_views.delete),
    path('applications/update_traitement/<int:id>/', applications_views.update_traitement),

    path('fiches/', fiches_views.index),
    path('fiches/update/<int:id>/', fiches_views.update),
    path('fiches/affiche/<int:id>/', fiches_views.affiche),
    path('fiches/traitement/', fiches_views.traitement),
    path('fiches/ajout/', fiches_views.ajout),
    path('fiches/delete/<int:id>/', fiches_views.delete),
    path('fiches/update_traitement/<int:id>/', fiches_views.update_traitement),
]
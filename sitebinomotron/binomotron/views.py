from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.utils import timezone
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from .group_crea import groupe_create

from .models import Apprenant, Brief, Groupe

# View pour la page d'accueil de l'API
def index(request) :
    return render(request, 'other/index.html')

# Partie Apprenant

# View pour la page des apprenants
def apprenantview(request) :
    # On affiche la liste des apprenants trier par le nom
    if request.method == 'GET' :
        apprenant_list = Apprenant.objects.all().order_by('nom')
        return render(request, 'apprenant/apprenant.html', {'apprenant_list' : apprenant_list})
    # Lorsque l'on effectue une recherche il s'agit d'une méthod post et on affiche les apprenants dont le nom
    # contient le motif de recherche
    elif request.method ==  'POST' :
        apprenant_list = Apprenant.objects.all().filter(nom__icontains=request.POST.get('search'))
        return render(request, 'apprenant/apprenant.html', {'apprenant_list' : apprenant_list})

# View pour le formulaire afin d'ajouter un apprenant
class ApprenantAddClass(SuccessMessageMixin, CreateView):
    model = Apprenant
    template_name = "apprenant/apprenant_add.html"
    fields = ['nom', 'prenom']
    
    # On retourne un message de succès et une création d'un apprenant réussie retourne sur la page affichant
    # la liste des apprenants
    success_message = "%(prenom)s %(nom)s ajouté avec succès!"
    def get_success_url(self, **kwargs):
        return reverse_lazy('binomotron:apprenant')

# View pour la modification des informations pour un apprenant
class ApprenantEditClass(SuccessMessageMixin, UpdateView):
    model = Apprenant
    fields = ['nom', 'prenom']
    template_name = "apprenant/apprenant_edit.html"
    
    # On retourne un message de succès et une modification d'un apprenant réussie retourne sur la page affichant
    # la liste des apprenants
    success_message = "%(prenom)s %(nom)s modifié avec succès!"
    def get_success_url(self, **kwargs):
        return reverse_lazy('binomotron:apprenant')

# View affichant les détails d'un apprenant
class ApprenantDetailView(generic.DetailView):
    model = Apprenant
    template_name = 'apprenant/apprenant_detail.html'

# View pour demander la confirmation de suppression d'un apprennant
class ApprenantDeleteView(SuccessMessageMixin, DeleteView):
    model = Apprenant
     
    # url de redirection et message de succès
    success_url ="/apprenant"
    success_message = "Éliminé avec succès! AU SUIVANT!!!" 
    template_name = "apprenant/apprenant_deleteconfirmation.html"


# Partie Brief

# View pour la page des briefs
def briefview(request) :
    # On affiche la liste des briefs trier par le nom
    if request.method == 'GET' :
        brief_list = Brief.objects.all().order_by('nom')
        return render(request, 'brief/brief.html', {'brief_list' : brief_list})
    # Lorsque l'on effectue une recherche il s'agit d'une méthod post et on affiche les briefs dont le nom
    # contient le motif de recherche
    elif request.method ==  'POST' :
        brief_list = Brief.objects.all().filter(nom__icontains=request.POST.get('search'))
        return render(request, 'brief/brief.html', {'brief_list' : brief_list})

# View pour le formulaire afin d'ajouter un brief
class BriefAddClass(SuccessMessageMixin, CreateView):
    model = Brief
    template_name = "brief/brief_add.html"
    # Sur la date de début et de fin on a un validateur pour bloquer la création d'un brief ayant des dates
    # antérieurs à la date du jour de création du brief
    # De plus la date de fin ne peut pas être antérieur à la date de début
    fields = ['nom', 'lien', 'nombre', 'date_debut', 'date_fin']
    
    # On retourne un message de succès et une création d'un brief réussie retourne sur la page affichant
    # la liste des briefs
    success_message = "%(nom)s ajouté avec succès!"
    def get_success_url(self, **kwargs):
        return reverse_lazy('binomotron:brief')

# View pour la modification des informations pour un brief
class BriefEditClass(SuccessMessageMixin, UpdateView):
    model = Brief
    
    # On affiche seulement les champs nom, lien et nombre car le validateur sur les dates 
    # bloque l'envoie du formulaire si les dates sont antérieurs à la date du jour
    fields = ['nom', 'lien', 'nombre']
    # fields = ['nom', 'lien', 'nombre', 'date_debut', 'date_fin']
    template_name = "brief/brief_edit.html"
    
    # On retourne un message de succès et une modification d'un brief réussie retourne sur la page affichant
    # la liste des briefs
    success_message = "%(nom)s modifié avec succès!"
    def get_success_url(self, **kwargs):
        return reverse_lazy('binomotron:brief')

    # On récupère et enregistre le nombre pour la taille des groupes d'apprenants avant qu'il soit modifié
    def get_context_data(self, **kwargs):
        pk = self.get_object()
        context = super().get_context_data(**kwargs)
        brief = Brief.objects.get(pk = pk.pk)

        context['ancien_nombre'] = brief.nombre
        return context
    
    # Si la taille des groupes d'apprenants est modifié (en comparant au nombre sauvegardé juste avant)
    # on supprime l'ensemble des groupes liés au brief modifié
    def post(self, request, *args: str, **kwargs):
        form_nb_appr = request.POST["ancien_nombre"]
        current_brief = self.get_object()
        previous_nombre = current_brief.nombre
        if previous_nombre != form_nb_appr:
            Groupe.objects.filter(brief = current_brief.pk).delete()

        return super().post(request, *args, **kwargs)

# View affichant les détails d'un brief
class BriefDetailView(generic.DetailView):
    model = Brief
    template_name = 'brief/brief_detail.html'
    
    # On récupère les groupes liés au brief sélectionné et on stocke ces listes de groupes d'apprenants
    # dans le contexte pour être utilisable dans la page html
    def get_context_data(self, **kwargs) :
        pk = self.get_object()
        context = super().get_context_data(**kwargs)
        groups = Groupe.objects.filter(brief = pk)
                
        group_list = {}

        for group in groups :
            student = group.apprenants.select_related()
            group_list[group.nom] =student
        context['group_list'] = group_list
        return context

# View pour demander la confirmation de suppression d'un brief
class BriefDeleteView(SuccessMessageMixin, DeleteView):
    model = Brief
     
    # url de redirection
    success_url ="/brief"
    success_message = "Éliminé avec succès! AU SUIVANT!!!" 
    template_name = "brief/brief_deleteconfirmation.html"

# Partie Groupe

# On appel la fonction qui crée les groupes et on redirige la vue directement sur la page du brief 
# dont on vient de créer les groupes
def groupecreate(request, pk) :
    groupe_create(pk)
    return HttpResponseRedirect(reverse('binomotron:brief_detail', args=[pk]))
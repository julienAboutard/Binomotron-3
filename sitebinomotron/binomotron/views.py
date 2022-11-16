from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.utils import timezone
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from .group_crea import groupe_create

from .models import Apprenant, Brief, Groupe

def index(request) :
    return render(request, 'other/index.html')

def apprenantview(request) :
    if request.method == 'GET' :
        apprenant_list = Apprenant.objects.all().order_by('nom')
        return render(request, 'apprenant/apprenant.html', {'apprenant_list' : apprenant_list})
    elif request.method ==  'POST' :
        apprenant_list = Apprenant.objects.all().filter(nom__icontains=request.POST.get('search'))
        return render(request, 'apprenant/apprenant.html', {'apprenant_list' : apprenant_list})

class ApprenantAddClass(SuccessMessageMixin, CreateView):
    model = Apprenant
    template_name = "apprenant/apprenant_add.html"
    fields = ['nom', 'prenom']
    
    success_message = "%(prenom)s %(nom)s ajouté avec succès!"
    def get_success_url(self, **kwargs):
        return reverse_lazy('binomotron:apprenant')
    
class ApprenantEditClass(SuccessMessageMixin, UpdateView):
    model = Apprenant
    fields = ['nom', 'prenom']
    template_name = "apprenant/apprenant_edit.html"
    
    success_message = "%(prenom)s %(nom)s modifié avec succès!"
    def get_success_url(self, **kwargs):
        return reverse_lazy('binomotron:apprenant')

class ApprenantDetailView(generic.DetailView):
    model = Apprenant
    template_name = 'apprenant/apprenant_detail.html'


class ApprenantDeleteView(SuccessMessageMixin, DeleteView):
    model = Apprenant
     
    # url de redirection
    success_url ="/apprenant"
    success_message = "Éliminé avec succès! AU SUIVANT!!!" 
    template_name = "apprenant/apprenant_deleteconfirmation.html"

# Partie Brief

def briefview(request) :
    if request.method == 'GET' :
        brief_list = Brief.objects.all().order_by('nom')
        return render(request, 'brief/brief.html', {'brief_list' : brief_list})
    elif request.method ==  'POST' :
        brief_list = Brief.objects.all().filter(nom__icontains=request.POST.get('search'))
        return render(request, 'brief/brief.html', {'brief_list' : brief_list})

class BriefAddClass(SuccessMessageMixin, CreateView):
    model = Brief
    template_name = "brief/brief_add.html"
    fields = ['nom', 'lien', 'nombre']
    
    success_message = "%(nom)s ajouté avec succès!"
    def get_success_url(self, **kwargs):
        return reverse_lazy('binomotron:brief')
    
class BriefEditClass(SuccessMessageMixin, UpdateView):
    model = Brief

    fields = ['nom', 'lien', 'nombre']
    template_name = "brief/brief_edit.html"
    
    success_message = "%(nom)s modifié avec succès!"

    def get_success_url(self, **kwargs):
        return reverse_lazy('binomotron:brief')

    def get_context_data(self, **kwargs):
        pk = self.get_object()
        context = super().get_context_data(**kwargs)
        brief = Brief.objects.get(pk = pk.pk)

        context['ancien_nombre'] = brief.nombre
        return context
    
    def post(self, request, *args: str, **kwargs):
        form_nb_appr = request.POST["ancien_nombre"]
        current_brief = self.get_object()
        previous_nombre = current_brief.nombre
        if previous_nombre != form_nb_appr:
            Groupe.objects.filter(brief = current_brief.pk).delete()

        return super().post(request, *args, **kwargs)

class BriefDetailView(generic.DetailView):
    model = Brief
    template_name = 'brief/brief_detail.html'
    
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


class BriefDeleteView(SuccessMessageMixin, DeleteView):
    model = Brief
     
    # url de redirection
    success_url ="/brief"
    success_message = "Éliminé avec succès! AU SUIVANT!!!" 
    template_name = "brief/brief_deleteconfirmation.html"


def groupecreate(request, pk) :
    groupe_create(pk)
    return redirect('/brief/%d'% pk)




from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.utils import timezone
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin

from .models import Apprenant, Brief, Groupe

def index(request) :
    return render(request, 'other/index.html')

def apprenantview(request) :
    if request.method == 'GET' :
        apprenant_list = Apprenant.objects.all().order_by('nom')
        return render(request, 'apprenant/apprenant.html', {'apprenant_list' : apprenant_list})
    elif request.method ==  'POST' :
        apprenant_list = Apprenant.objects.all().filter(nom=request.POST.get('search'))
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
    template_name = 'apprenant/detail.html'


class ApprenantDeleteView(SuccessMessageMixin, DeleteView):
    model = Apprenant
     
    # url de redirection
    success_url ="/apprenant"
    success_message = "Éliminé avec succès! AU SUIVANT!!!" 
    template_name = "apprenant/deleteconfirmation.html"


# Essaie de faire une view pour la liste d'apprenant sous forme de classe héritant de ListView
# class ApprenantView(generic.ListView):
#     model = Apprenant
#     template_name = 'apprenant/apprenant.html'
#     context_object_name = 'apprenant_list'

#     def post(self, request): 
#         self.object_list = self.get_queryset() 
#         return HttpResponseRedirect(reverse('binomotron:apprenant'))

#     def get_queryset(self):

#         if self.request.method == 'POST' :
#             return Apprenant.objects.all().order_by('prenom')
            
#         else :
#             return Apprenant.objects.all().order_by('nom')
        

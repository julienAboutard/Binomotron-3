from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Apprenant, Brief, Groupe

def index(request) :
    return render(request, 'other/index.html')

class ApprenantView(generic.ListView):
    template_name = 'apprenant/apprenant.html'
    context_object_name = 'apprenant_list'

    def post(self, request):  # ***** this method required! ******
        self.object_list = self.get_queryset() 
        return HttpResponseRedirect(reverse('binomotron:apprenant'))

    def get_queryset(self):
        """
        Return the last five added apprenants (not including those set to be
        published in the future).
        """

        if self.request.method == "GET" :
            return Apprenant.objects.order_by('nom').all()
        
        elif self.request.method == "POST" : 
            # return Apprenant.objects.filter(nom__exact = self.request.POST.get('search')).all()
            return Apprenant.objects.order_by('prenom').all()
    
class ApprenantDetailView(generic.DetailView):
    model = Apprenant
    template_name = 'apprenant/detail.html'
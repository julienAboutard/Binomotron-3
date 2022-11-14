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

    def get_queryset(self):
        """
        Return the last five added apprenants (not including those set to be
        published in the future).
        """
        return Apprenant.objects.order_by('nom')
    
class ApprenantDetailView(generic.DetailView):
    model = Apprenant
    template_name = 'apprenant/detail.html'
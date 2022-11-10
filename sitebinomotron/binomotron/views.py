from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Apprenant, Brief, Groupe


class ApprenantView(generic.ListView):
    template_name = 'polls/apprenant.html'
    context_object_name = 'latest_apprenant_list'

    def get_queryset(self):
        """
        Return the last five added apprenants (not including those set to be
        published in the future).
        """
        return Apprenant.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]
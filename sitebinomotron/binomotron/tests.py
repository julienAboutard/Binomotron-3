from django.test import TestCase
from .models import Apprenant, Brief, Groupe
from .group_crea import groupe_create
from django.shortcuts import get_object_or_404
from django.utils import timezone

class ApprenantTestCase(TestCase) :
    def setUp(self) :
        Apprenant.objects.create(nom='Aboutard', prenom='Julien')
        Apprenant.objects.create(nom='Costes', prenom='Audrey')

    def apprenant_exist_test(self) :
        # Vérifier que les apprenants créer dans le setUp() existent bien 
        julien = get_object_or_404(Apprenant, pk=1)
        audrey = get_object_or_404(Apprenant, pk=2)
        test404 = get_object_or_404(Apprenant, pk=3)

        self.assertEqual(julien.nom, "Aboutard")
        self.assertEqual(julien.prenom, "Julien")
        self.assertEqual(audrey.nom, "Costes")
        self.assertEqual(audrey.prenom, "Audrey")
        self.assertHTMLEqual(test404, 404)

# class BriefTestCase(TestCase) :

#     def setUp(self) :
#         Brief.objects.create(nom='pouet', lien='http://pouet.co', nombre=3)
#         Brief.objects.create(nom='essaie', lien='http://essaie.co', date_debut='2022-11-20', date_fin ='2022-11-25')
    
#     def brief_exist_test(self) :
#         brief1 = get_object_or_404(Brief, pk=1)
#         brief2 = get_object_or_404(Brief, pk=2)

#         self.assertEqual(brief1.lien, "http://pouet.co")
#         self.assertEqual(brief1.nom, 'pouet')
#         self.assertEqual(brief1.nombre, 3)
#         self.assertEqual(brief1.date_debut, timezone.now().date())
#         self.assertEqual(brief1.date_fin, timezone.now().date())
#         self.assertEqual(brief1.lien, "http://essaie.co")
#         self.assertEqual(brief1.nom, 'essaie')
#         self.assertEqual(brief1.nombre, 2)
#         self.assertEqual(brief1.date_debut, '2022-11-20')
#         self.assertEqual(brief1.date_fin, '2022-11-25')


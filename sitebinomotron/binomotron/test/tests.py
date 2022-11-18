import datetime

from django.test import TestCase
from ..models import Apprenant, Brief, Groupe
from ..group_crea import groupe_create
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import IntegrityError


class BriefFormModelTests(TestCase):

    # Raise une erreur si un brief est créé avec le même url qu'un brief existant
    def test_brief_already_exists(self):

        brief1 = Brief.objects.create(nom = "brief1", lien = "https://www.brief1.fr")

        # lorsqu'un brief est créé et qu'un nouveau brief ayant le même url tente d'être créé, IntegrityError est signalé
        with self.assertRaises(IntegrityError):
            # ici, si IntegrityError est raise lors de la création du brief2 alors la vérification fonctionne et le brief n'est pas créé
            Brief.objects.create(nom = "brief2", lien = "https://www.brief1.fr")


class ApprenantTestCase(TestCase) :
    def setUp(self) :
        # Remplir la base de données pour les tests
        Apprenant.objects.create(nom='Aboutard', prenom='Julien')
        Apprenant.objects.create(nom='Costes', prenom='Audrey')

    def test_apprenant_exist(self) :
        # Vérifier que les apprenants créer dans le setUp() existent bien 
        julien = get_object_or_404(Apprenant, pk=1)
        audrey = get_object_or_404(Apprenant, pk=2)

        self.assertEqual(julien.nom, "Aboutard")
        self.assertEqual(julien.prenom, "Julien")
        self.assertEqual(audrey.nom, "Costes")
        self.assertEqual(audrey.prenom, "Audrey")


class BriefTestCase(TestCase) :

    def setUp(self) :
        # Remplir la base de données pour les tests
        Brief.objects.create(nom='pouet', lien='http://pouet.co', nombre=3)
        Brief.objects.create(nom='essaie', lien='http://essaie.co', date_debut='2022-11-20', date_fin ='2022-11-25')
    
    def test_brief_exist(self) :
        # Vérifier que les Briefs créer dans le setUp() existent bien 
        brief1 = get_object_or_404(Brief, pk=1)
        brief2 = get_object_or_404(Brief, pk=2)

        self.assertEqual(brief1.lien, "http://pouet.co")
        self.assertEqual(brief1.nom, 'pouet')
        self.assertEqual(brief1.nombre, 3)
        self.assertEqual(brief1.date_debut, timezone.now().date())
        self.assertEqual(brief1.date_fin, timezone.now().date())
        self.assertEqual(brief2.lien, "http://essaie.co")
        self.assertEqual(brief2.nom, 'essaie')
        self.assertEqual(brief2.nombre, 2)
        self.assertEqual(brief2.date_debut, datetime.date(2022, 11, 20))
        self.assertEqual(brief2.date_fin, datetime.date(2022, 11, 25))


class GroupeCreationTests(TestCase) :

    def setUp(self):
        # Remplir la base de données pour les tests
        Apprenant.objects.create(nom='Aboutard', prenom='Julien')
        Apprenant.objects.create(nom='Costes', prenom='Audrey')
        Apprenant.objects.create(nom='Paris', prenom='Dorine')
        Apprenant.objects.create(nom='Boettcher', prenom='Vincent')

        Brief.objects.create(nom='Pouet', lien='http://pouet.fr', nombre=2)
        
    def test_groupe_create(self) :
        # Vérifier que lorsque l'on crée des groupes, ils existent bien et les apprenants sont bien attribués
        brief1 = get_object_or_404(Brief, nom='Pouet')
        groupe_create(brief1.pk)
        groupes = Groupe.objects.filter(brief = brief1.pk)
        self.assertIsNotNone(groupes)
        self.assertEqual(groupes.count(), 2)

        for groupe in groupes:
            students = groupe.apprenants.select_related()
            self.assertEqual(students.count(), 2)
        
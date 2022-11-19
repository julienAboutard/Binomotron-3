import datetime

from django.test import TestCase
from ..models import Apprenant, Brief, Groupe
from ..group_crea import groupe_create
from django.shortcuts import get_object_or_404, get_list_or_404
from django.utils import timezone
from django.db import IntegrityError
from django.urls import reverse
from django.http import Http404


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
        Apprenant.objects.create(nom='Paris', prenom='Dorine')

    def test_apprenant_exist(self) :
        # Vérifier que les apprenants créer dans le setUp() existent bien 
        julien = get_object_or_404(Apprenant, prenom='Julien')
        audrey = get_object_or_404(Apprenant, prenom='Audrey')

        self.assertEqual(julien.nom, "Aboutard")
        self.assertEqual(julien.prenom, "Julien")
        self.assertEqual(audrey.nom, "Costes")
        self.assertEqual(audrey.prenom, "Audrey")

    def test_apprenant_update(self):
        #Vérifier qu'une modification est bien enregistré 
        julien = get_object_or_404(Apprenant, nom='Aboutard')
        julien.prenom='Aurélien'
        julien.save()

        appr= get_object_or_404(Apprenant, nom='Aboutard')
        self.assertEqual(appr.nom, "Aboutard")
        self.assertEqual(appr.prenom, "Aurélien")

    def test_apprenant_delete(self):
        # Vérifier qu'une suppression d'un apprenant est bien enregistré
        Apprenant.objects.filter(nom='Aboutard').delete()
        with self.assertRaises(Http404):
            get_object_or_404(Apprenant, nom='Aboutard')
        with self.assertRaises(Apprenant.DoesNotExist):
            Apprenant.objects.get(nom='Aboutard')
    




class BriefTestCase(TestCase) :

    def setUp(self) :
        # Remplir la base de données pour les tests
        Brief.objects.create(nom='pouet', lien='http://pouet.co', nombre=3)
        Brief.objects.create(nom='essaie', lien='http://essaie.co', date_debut='2022-11-20', date_fin ='2022-11-25')
    
    def test_brief_exist(self) :
        # Vérifier que les Briefs créer dans le setUp() existent bien 
        brief1 = get_object_or_404(Brief, nom='pouet')
        brief2 = get_object_or_404(Brief, nom='essaie')

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
    
    def test_brief_update(self):
        # Vérifier qu'une modification de brief est bien enregistré 
        brief1 = get_object_or_404(Brief, nom='pouet')
        brief1.nom='pouet2'
        brief1.save()

        brief= get_object_or_404(Brief, nom='pouet2')
        self.assertEqual(brief.nom, "pouet2")
        self.assertEqual(brief.lien, "http://pouet.co")
        self.assertEqual(brief.nombre, 3)
        self.assertEqual(brief.date_debut, timezone.now().date())
        self.assertEqual(brief.date_fin, timezone.now().date())

    def test_brief_delete(self):
        # Vérifier qu'une suppression d'un brief est bien enregistré
        Brief.objects.filter(nom='pouet').delete()
        with self.assertRaises(Http404):
            get_object_or_404(Brief, nom='pouet')
        with self.assertRaises(Brief.DoesNotExist):
            Brief.objects.get(nom='pouet')


class GroupeTestCase(TestCase) :

    def setUp(self):
        # Remplir la base de données pour les tests
        Apprenant.objects.create(nom='Aboutard', prenom='Julien')
        Apprenant.objects.create(nom='Costes', prenom='Audrey')
        Apprenant.objects.create(nom='Paris', prenom='Dorine')
        Apprenant.objects.create(nom='Boettcher', prenom='Vincent')

        self.brief1 = Brief.objects.create(nom='Pouet', lien='http://pouet.fr', nombre=2)

        groupe_create(self.brief1.pk)
 
        
    def test_groupe_create(self) :
        # Vérifier que lorsque l'on crée des groupes, ils existent bien et les apprenants sont bien attribués
        groupes = Groupe.objects.filter(brief = self.brief1.pk)
        self.assertIsNotNone(groupes)
        self.assertEqual(groupes.count(), 2)

        for groupe in groupes:
            students = groupe.apprenants.select_related()
            self.assertEqual(students.count(), 2)
    
    def test_groupe_update(self):
        # On test que la modification du nom de groupe soit bien enregistrée
        groupes = get_list_or_404(Groupe, brief = self.brief1.pk)
        groupes[0].nom = "Dream Team"
        groupes[0].save()

        groupes_modif = get_list_or_404(Groupe, brief = self.brief1.pk)
        self.assertEqual(groupes_modif[0].nom, "Dream Team")
    
    def test_groupe_brief_delete(self):
        # On vérifie que la suppression d'un brief supprime tous les groupes liés
        self.brief1.delete()

        with self.assertRaises(Http404):
            get_list_or_404(Groupe, brief = self.brief1.pk)

        

class RedirectTestCase(TestCase) :
    # Dans cette Classe de test on va vérifier qu'une des urls du site affiche bien une page et utlise le bon template
    def setUp(self) :
        Apprenant.objects.create(nom='Costes', prenom='Audrey')
        Brief.objects.create(nom='Pouet', lien='http://pouet.fr', nombre=2)

    def test_redirect_index(self):
        response = self.client.get(reverse('binomotron:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "other/index.html")
    
    def test_redirect_apprenant(self):
        response = self.client.get(reverse('binomotron:apprenant'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "apprenant/apprenant.html")
    
    def test_redirect_brief(self):
        response = self.client.get(reverse('binomotron:brief'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "brief/brief.html")
    
    def test_redirect_brief_detail(self): 
        brief1 = get_object_or_404(Brief, nom='Pouet')
        response = self.client.get(reverse('binomotron:brief_detail', args=[brief1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "brief/brief_detail.html")
    
    def test_redirect_apprenant_detail(self): 
        apprenant1 = get_object_or_404(Apprenant, prenom='Audrey')
        response = self.client.get(reverse('binomotron:apprenant_detail', args=[apprenant1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "apprenant/apprenant_detail.html")
    
    def test_redirect_brief_add(self): 
        response = self.client.get(reverse('binomotron:brief_add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "brief/brief_add.html")

    def test_redirect_apprenant_add(self): 
        response = self.client.get(reverse('binomotron:apprenant_add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "apprenant/apprenant_add.html")
    
    def test_redirect_brief_edit(self): 
        brief1 = get_object_or_404(Brief, nom='Pouet')
        response = self.client.get(reverse('binomotron:brief_edit', args=[brief1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "brief/brief_edit.html")
    
    def test_redirect_apprenant_edit(self): 
        apprenant1 = get_object_or_404(Apprenant, prenom='Audrey')
        response = self.client.get(reverse('binomotron:apprenant_edit', args=[apprenant1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "apprenant/apprenant_edit.html")

    def test_redirect_brief_supprimer(self): 
        brief1 = get_object_or_404(Brief, nom='Pouet')
        response = self.client.get(reverse('binomotron:supprimer-brief', args=[brief1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "brief/brief_deleteconfirmation.html")
    
    def test_redirect_apprenant_supprimer(self): 
        apprenant1 = get_object_or_404(Apprenant, prenom='Audrey')
        response = self.client.get(reverse('binomotron:supprimer-apprenant', args=[apprenant1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "apprenant/apprenant_deleteconfirmation.html")
        
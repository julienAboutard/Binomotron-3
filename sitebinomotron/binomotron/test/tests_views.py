from django.test import TestCase
from django.urls import reverse
from django.db.models import QuerySet
import pprint

from ..models import Brief, Groupe, Apprenant

class ViewTest(TestCase):

# déclaration d'une BDD fictionnelle
    def setUp(self):
        self.audrey = Apprenant.objects.create(nom='Costes', prenom='Audrey')
        self.dorine = Apprenant.objects.create(nom='Paris', prenom='Dorine')
        self.julien = Apprenant.objects.create(nom='Aboutard', prenom='Julien')
        self.vincent = Apprenant.objects.create(nom='Boettcher', prenom='Vincent')
        self.djamila = Apprenant.objects.create(nom='Chabane', prenom='Djamila')
        self.alice = Apprenant.objects.create(nom='Lafon', prenom='Alice')

        self.briefA = Brief.objects.create(nom='Titanic', lien='https://titanic.com', nombre=2)
        self.briefB = Brief.objects.create(nom='YAB', lien='https://yab.com', nombre=3)

        self.groupeA = Groupe.objects.create(nom='Dream Team', brief=self.briefB)
        self.groupeA = Groupe.objects.create(nom='Dream Team', brief=self.briefB)
        self.groupeA = Groupe.objects.create(nom='Dream Team', brief=self.briefB)
        self.groupeA = Groupe.objects.create(nom='Dream Team', brief=self.briefB)

        self.groupeB = Groupe.objects.create(nom='Team Rocket', brief=self.briefA)
        self.groupeB = Groupe.objects.create(nom='Team Rocket', brief=self.briefA)
        
        self.groupeC = Groupe.objects.create(nom='Team & Jerry', brief=self.briefA)
        self.groupeC = Groupe.objects.create(nom='Team & Jerry', brief=self.briefA)
        
        self.groupeD = Groupe.objects.create(nom='Potateam', brief=self.briefA)
        self.groupeD = Groupe.objects.create(nom='Potateam', brief=self.briefA)


        self.liaison1 = self.groupeA.apprenants.add(self.audrey)
        self.liaison2 = self.groupeA.apprenants.add(self.dorine)
        self.liaison3 = self.groupeA.apprenants.add(self.vincent)
        self.liaison4 = self.groupeA.apprenants.add(self.julien)

        self.liaison5 = self.groupeB.apprenants.add(self.djamila)
        self.liaison6 = self.groupeB.apprenants.add(self.audrey)

        self.liaison7 = self.groupeC.apprenants.add(self.dorine)
        self.liaison8 = self.groupeC.apprenants.add(self.alice)

        self.liaison9 = self.groupeD.apprenants.add(self.julien)
        self.liaison10 = self.groupeD.apprenants.add(self.vincent)

# Vérification vue Index : index.html
    def test_index_view(self):
        response = self.client.get(reverse('binomotron:index'))
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'other/index.html')

# Vérification des vues Apprenant :

    # apprenant_detail.html
    def test_apprenant_detail_view(self):
        a = Apprenant.objects.get(nom="Costes")

        response = self.client.get(reverse('binomotron:apprenant_detail', kwargs={'pk': a.id}))
        # pris en charge par django
        # self.assertEqual(type(response.context.get('object')), Apprenant)
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'apprenant/apprenant_detail.html')
    
    # apprenant.html
    def test_apprenant_list_view(self):
        # print([b.id for b in Brief.objects.all()])

        response = self.client.get(reverse('binomotron:apprenant'))
        self.assertEqual(type(response.context.get('apprenant_list')), QuerySet)
        self.assertContains(response, ">Recherche</button>")
        self.assertContains(response, ">Ajouter</button>")
        self.assertContains(response, ">Modifier</button>", count= response.context.get('apprenant_list').count())
        self.assertContains(response, ">Supprimer</button>", count= response.context.get('apprenant_list').count())
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'apprenant/apprenant.html')

# Vérification des vues Brief :

    # brief_detail.html
    def test_brief_detail_view(self):
        briefs = Brief.objects.all()
        # print(briefs)
        # print([b.id for b in briefs])
        b = Brief.objects.get(nom="YAB")
        response = self.client.get(reverse('binomotron:brief_detail', kwargs={'pk': b.id}))
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(response.context)

        # pris en charge par django
        # self.assertEqual(type(response.context.get('object')), Brief)
        # self.assertEqual(type(response.context.get('group_list')), dict)

        # for key, value in response.context.get('group_list').items():
        #     self.assertEqual(type(value), QuerySet)

        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'brief/brief_detail.html')
    
    # brief.html
    def test_brief_list_view(self):
        response = self.client.get(reverse('binomotron:brief'))
        self.assertEqual(type(response.context.get('brief_list')), QuerySet)
        self.assertContains(response, ">Recherche</button>")
        self.assertContains(response, ">Ajouter</button>")
        self.assertContains(response, ">Modifier</button>", count= response.context.get('brief_list').count())
        self.assertContains(response, ">Supprimer</button>", count= response.context.get('brief_list').count())
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'brief/brief.html')


#     # def test_apprenant_detail_view(self):
#     #     response = self.client.get(reverse('binomotron:apprenant_detail'))
#     #     self.assertEqual(type(response.context.get('backlogs')), QuerySet)
#     #     self.assertEqual(len(response.context.get('backlogs')), 2)
#     #     self.assertEqual(type(response.context.get('teams')), QuerySet)
#     #     self.assertEqual(len(response.context.get('teams')), 2)
#     #     self.failUnlessEqual(response.status_code, 200)
    

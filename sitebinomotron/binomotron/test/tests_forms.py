from django.test import TestCase
from django.urls import reverse
from django.db.models import QuerySet
import pprint
import datetime


from ..models import Brief, Groupe, Apprenant

#### tests sur le mauvais renseignement de champs dans les formulaires

class FormTest(TestCase):

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


######### FORMULAIRES BRIEF

# tests formulaire de création de briefs

    def test_brief_add_post_nombre_non_valide_view(self):
        response = self.client.post(reverse('binomotron:brief_add'), data={
            'nom': "pouet", 'lien': "http://pouet.co", 'nombre':"kqijf"
        })
        status_code = response.status_code
        # print("##########################")
        # print(type(response))
        # print(dir(response))
        # print("##########################")
        self.assertContains(response, 'class="errorlist"')
        self.failUnlessEqual(status_code, 200)
        self.assertTemplateUsed(response, 'brief/brief_add.html')

    def test_brief_add_post_nombre_negatif_view(self):
        response = self.client.post(reverse('binomotron:brief_add'), data={
            'nom': "pouet", 'lien': "http://pouet.co", 'nombre':-1
        })
        # self.assertInHTML('class="errorlist"', response.content)
        self.assertContains(response, 'class="errorlist"')
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'brief/brief_add.html')

    def test_brief_add_post_nombre_nulle_view(self):
        response = self.client.post(reverse('binomotron:brief_add'), data={
            'nom': "pouet", 'lien': "http://pouet.co", 'nombre':0
        })
        self.assertContains(response, 'class="errorlist"')
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'brief/brief_add.html')

    def test_brief_add_post_nombre_inf_a_2_view(self):
        response = self.client.post(reverse('binomotron:brief_add'), data={
            'nom': "pouet", 'lien': "http://pouet.co", 'nombre':1
        })
        self.assertContains(response, 'class="errorlist"')
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'brief/brief_add.html')

    def test_brief_add_post_url_non_valide_view(self):
        response = self.client.post(reverse('binomotron:brief_add'), data={
            'nom': "pouet", 'lien': "pouet.co", 'nombre':2
        })
        self.assertContains(response, 'class="errorlist"')
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'brief/brief_add.html')

    def test_brief_add_post_chaine_trop_longue_non_valide_view(self):
        response = self.client.post(reverse('binomotron:brief_add'), data={
            'nom': "ojvloneqmbvnqùeb nqùdnvf eqjvqkdjnfdbùqdnbjqùbqnv jfq qjfd nbùnfq !f !sjf !fsj kjfq kjs nfv n%SF ", 'lien': "http://pouet.co", 'nombre':2
        })
        self.assertContains(response, 'class="errorlist"')
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'brief/brief_add.html')

    def test_brief_add_post_chaine_trop_courte_non_valide_view(self):
        response = self.client.post(reverse('binomotron:brief_add'), data={
            'nom': "", 'lien': "http://pouet.co", 'nombre':2
        })
        self.assertContains(response, 'class="errorlist"')
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'brief/brief_add.html')

    def test_brief_add_post_date_debut_passe_non_valide_view(self):
        response = self.client.post(reverse('binomotron:brief_add'), data={
            'nom': "YAB", 'lien': "http://pouet.co", 'nombre':2, 'date_debut':datetime.datetime(2022, 11, 18)
        })
        self.assertContains(response, 'class="errorlist')
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'brief/brief_add.html')

    def test_brief_add_post_date_fin_passe_non_valide_view(self):
        response = self.client.post(reverse('binomotron:brief_add'), data={
            'nom': "YAB", 'lien': "http://pouet.co", 'nombre':2, 'date_fin':datetime.datetime(2022, 11, 18)
        })
        self.assertContains(response, 'class="errorlist')
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'brief/brief_add.html')

    def test_brief_add_post_date_debut_apres_date_fin_non_valide_view(self):
        response = self.client.post(reverse('binomotron:brief_add'), data={
            'nom': "YAB", 'lien': "http://pouet.co", 'nombre':2, 'date_debut':datetime.datetime(2022, 12, 23), 'date_fin':datetime.datetime(2022, 11, 21)
        })
        self.assertContains(response, 'class="errorlist')
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'brief/brief_add.html')



# tests formulaire de modification de briefs

    def test_brief_edit_post_nombre_non_valide_view(self):
        b = Brief.objects.get(nom="YAB")

        response = self.client.post(reverse('binomotron:brief_edit', args=[b.pk]), data={
            'nombre':"kqijf", 'ancien_nombre':b.nombre
        })
        status_code = response.status_code
        self.assertContains(response, 'class="errorlist"')
        self.failUnlessEqual(status_code, 200)
        self.assertTemplateUsed(response, 'brief/brief_edit.html')

    def test_brief_edit_post_nombre_negatif_view(self):
        b = Brief.objects.get(nom="YAB")
        response = self.client.post(reverse('binomotron:brief_edit', args=[b.pk]), data={
            'nombre':-1, 'ancien_nombre':b.nombre
        })
        # self.assertInHTML('class="errorlist"', response.content)
        self.assertContains(response, 'class="errorlist"')
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'brief/brief_edit.html')

    def test_brief_edit_post_nombre_nulle_view(self):
        b = Brief.objects.get(nom="YAB")
        response = self.client.post(reverse('binomotron:brief_edit', args=[b.pk]), data={
            'nombre':0, 'ancien_nombre':b.nombre
        })
        self.assertContains(response, 'class="errorlist"')
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'brief/brief_edit.html')

    def test_brief_edit_post_nombre_inf_a_2_view(self):
        b = Brief.objects.get(nom="YAB")
        response = self.client.post(reverse('binomotron:brief_edit', args=[b.pk]), data={
            'nombre':1, 'ancien_nombre':b.nombre
        })
        self.assertContains(response, 'class="errorlist"')
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'brief/brief_edit.html')

    def test_brief_edit_post_url_non_valide_view(self):
        b = Brief.objects.get(nom="YAB")
        response = self.client.post(reverse('binomotron:brief_edit', args=[b.pk]), data={
            'lien': "pouet.co", 'ancien_nombre':b.nombre
        })
        self.assertContains(response, 'class="errorlist"')
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'brief/brief_edit.html')

    def test_brief_edit_post_chaine_trop_longue_non_valide_view(self):
        b = Brief.objects.get(nom="YAB")
        response = self.client.post(reverse('binomotron:brief_edit', args=[b.pk]), data={
            'nom': "ojvloneqmbvnqùeb nqùdnvf eqjvqkdjnfdbùqdnbjqùbqnv jfq qjfd nbùnfq !f !sjf !fsj kjfq kjs nfv n%SF ", 'ancien_nombre':b.nombre
        })
        self.assertContains(response, 'class="errorlist"')
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'brief/brief_edit.html')

    def test_brief_edit_post_chaine_trop_courte_non_valide_view(self):
        b = Brief.objects.get(nom="YAB")
        response = self.client.post(reverse('binomotron:brief_edit', args=[b.pk]), data={
            'nom': "", 'ancien_nombre':b.nombre
        })
        self.assertContains(response, 'class="errorlist"')
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'brief/brief_edit.html')

    def test_brief_edit_post_date_debut_passe_non_valide_view(self):
        b = Brief.objects.get(nom="YAB")
        response = self.client.post(reverse('binomotron:brief_edit', args=[b.pk]), data={
            'date_debut':datetime.datetime(2022, 11, 18), 'ancien_nombre':b.nombre
        })
        self.assertContains(response, 'class="errorlist')
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'brief/brief_edit.html')

    def test_brief_edit_post_date_fin_passe_non_valide_view(self):
        b = Brief.objects.get(nom="YAB")
        response = self.client.post(reverse('binomotron:brief_edit', args=[b.pk]), data={
            'date_fin':datetime.datetime(2022, 11, 18), 'ancien_nombre':b.nombre
        })
        self.assertContains(response, 'class="errorlist')
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'brief/brief_edit.html')

    def test_brief_edit_post_date_debut_apres_date_fin_non_valide_view(self):
        b = Brief.objects.get(nom="YAB")
        response = self.client.post(reverse('binomotron:brief_edit', args=[b.pk]), data={
            'date_debut':datetime.datetime(2022, 12, 23), 'date_fin':datetime.datetime(2022, 11, 21), 'ancien_nombre':b.nombre
        })
        self.assertContains(response, 'class="errorlist')
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'brief/brief_edit.html')

######### FORMULAIRES APPRENANTS

# tests formulaire de création d'apprenants

    def test_apprenant_add_post_prenom_vide_view(self):
        response = self.client.post(reverse('binomotron:apprenant_add'), data={
            'nom': "Paris", 'prenom':''
        })
        self.assertContains(response, 'class="errorlist')
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'apprenant/apprenant_add.html')

    def test_apprenant_add_prenom_trop_long_view(self):
        response = self.client.post(reverse('binomotron:apprenant_add'), data={
            'nom': "Paris", 'prenom':'ldesfnlnvlsknvksnvlsnvlsknvlksdnvlksdnvlksndvlksndlkvsndlkvsnlvknslkvnlkdsnvkdsnvlksnvlksdnvmksdnbmsknbmksnblkfdsnvlsnlkfdnblksnblksndlkfdskbnldwnblwdnblw!wnblw!wnwnlbdfwfdgfdgfdsvdnsldnvlknvlkqndlknvlqnvlkdnllwdkjvbkdjbvkjdbvkwjbvkwbkjvbkwbvkjwbkjb'
        })
        self.assertContains(response, 'class="errorlist')
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'apprenant/apprenant_add.html')

    def test_apprenant_add_post_nom_vide_view(self):
        response = self.client.post(reverse('binomotron:apprenant_add'), data={
            'nom': "", 'prenom':'Dorine'
        })
        self.assertContains(response, 'class="errorlist')
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'apprenant/apprenant_add.html')

    def test_apprenant_add_nom_trop_long_view(self):
        response = self.client.post(reverse('binomotron:apprenant_add'), data={
            'nom': "ldesfnlnvlsknvksnvlsnvlsknvlksdnvlksdnvlksndvlksndlkvsndlkvsnlvknslkvnlkdsnvkdsnvlksnvlksdnvmksdnbmsknbmksnblkfdsnvlsnlkfdnblksnblksndlkfdskbnldwnblwdnblw!wnblw!wnwnlbdfwfdgfdgfdsvdnsldnvlknvlkqndlknvlqnvlkdnllwdkjvbkdjbvkjdbvkwjbvkwbkjvbkwbvkjwbkjb", 'prenom':'Dorine'
        })
        self.assertContains(response, 'class="errorlist')
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'apprenant/apprenant_add.html')

# tests formulaire de modification d'apprenants

    def test_apprenant_edit_post_prenom_vide_view(self):
        a = Apprenant.objects.get(nom="Paris")

        response = self.client.post(reverse('binomotron:apprenant_edit', args=[a.pk]), data={
            'prenom':''
        })
        self.assertContains(response, 'class="errorlist')
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'apprenant/apprenant_edit.html')

    def test_apprenant_edit_prenom_trop_long_view(self):
        a = Apprenant.objects.get(nom="Paris")
        response = self.client.post(reverse('binomotron:apprenant_edit', args=[a.pk]), data={
            'nom':'Paris', 'prenom':'ldesfnlnvlsknvksnvlsnvlsknvlksdnvlksdnvlksndvlksndlkvsndlkvsnlvknslkvnlkdsnvkdsnvlksnvlksdnvmksdnbmsknbmksnblkfdsnvlsnlkfdnblksnblksndlkfdskbnldwnblwdnblw!wnblw!wnwnlbdfwfdgfdgfdsvdnsldnvlknvlkqndlknvlqnvlkdnllwdkjvbkdjbvkjdbvkwjbvkwbkjvbkwbvkjwbkjb'
        })
        self.assertContains(response, 'class="errorlist')
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'apprenant/apprenant_edit.html')

    def test_apprenant_edit_post_prenom_vide_view(self):
        a = Apprenant.objects.get(nom="Paris")
        response = self.client.post(reverse('binomotron:apprenant_edit', args=[a.pk]), data={
            'nom': ""
        })
        self.assertContains(response, 'class="errorlist')
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'apprenant/apprenant_edit.html')
    
    def test_apprenant_edit_nom_trop_long_view(self):
        a = Apprenant.objects.get(nom="Paris")
        response = self.client.post(reverse('binomotron:apprenant_edit', args=[a.pk]), data={
            'nom': "ldesfnlnvlsknvksnvlsnvlsknvlksdnvlksdnvlksndvlksndlkvsndlkvsnlvknslkvnlkdsnvkdsnvlksnvlksdnvmksdnbmsknbmksnblkfdsnvlsnlkfdnblksnblksndlkfdskbnldwnblwdnblw!wnblw!wnwnlbdfwfdgfdgfdsvdnsldnvlknvlkqndlknvlqnvlkdnllwdkjvbkdjbvkjdbvkwjbvkwbkjvbkwbvkjwbkjb", 'prenom':'Dorine'
        })
        self.assertContains(response, 'class="errorlist')
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'apprenant/apprenant_edit.html')
from django.test import TestCase
from .models import Apprenant, Brief, Groupe
from .group_crea import groupe_create
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


from django.db import models
from django.utils import timezone

class Apprenant(models.Model):
    nom = models.CharField(max_length=200)
    prenom = models.CharField(max_length=200)
    # pub_date = models.DateTimeField('date published')

    def __str__(self):
        return f"{self.nom} {self.prenom}"

class Brief(models.Model):
    nom = models.CharField(max_length=200)
    lien = models.CharField(max_length=200)
    nombre = models.SmallIntegerField(default=2)
    date_debut = models.DateTimeField(default = timezone.now())
    date_fin = models.DateTimeField(default = timezone.now())
    # pub_date = models.DateTimeField('date published')

    def __str__(self):
        return f"{self.nom}, groupes de {self.nombre} personnes"


class Groupe(models.Model):
    nom = models.CharField(max_length=200)
    brief = models.ForeignKey(Brief, on_delete=models.CASCADE)
    apprenants = models.ManyToManyField(Apprenant)


    def __str__(self):
        return f"{self.nom},brief {self.brief}"
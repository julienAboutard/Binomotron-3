from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator 

# Modèle django pour la Table SQl Apprenant
class Apprenant(models.Model):
    nom = models.CharField(max_length=200, null=True)
    prenom = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"

# Modèle django pour la Table SQl Brief
class Brief(models.Model):
    nom = models.CharField(max_length=200, null=True)
    lien = models.CharField(max_length=200, unique=True)
    # Pour la taille des n-omes on accepte que des valeurs supérieurs ou égales à 2 
    nombre = models.PositiveIntegerField(default=2, validators = [MinValueValidator(2)])
    # Indique la date de début et de fin d'un brief 
    # (amélioration => bloquer la création de brief dont la date de début ou de fin est antérieur à la date du jour de création)
    date_debut = models.DateField(default = timezone.now)
    date_fin = models.DateField(default = timezone.now)

    def __str__(self):
        return f"{self.nom}, groupes de {self.nombre} personnes"

# Modèle django pour la Table SQl Groupe
class Groupe(models.Model):
    nom = models.CharField(max_length=200, null=True)
    # Entre Brief et Groupe il y a une relation de 1 to many et on décide d'indiquer cette relation dans le modèle Groupe
    brief = models.ForeignKey(Brief, on_delete=models.CASCADE)
    # Entre Apprenant et Groupe, il y a une relation de many to many et on décide d'indiquer cette relation dans Groupe
    apprenants = models.ManyToManyField(Apprenant)


    def __str__(self):
        return f"{self.nom},brief {self.brief}"
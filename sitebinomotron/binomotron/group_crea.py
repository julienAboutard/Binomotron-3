import random

from .models import Apprenant, Brief, Groupe
from django.shortcuts import get_object_or_404, get_list_or_404



def groupe_create(brief_id):
    # Récupération de l'ensembles des apprenants et du brief concerné et s'ils n'existent pas on retourne un erreur 404
    students = get_list_or_404(Apprenant)
    brief_selec = get_object_or_404(Brief, pk = brief_id)
    
    res = []
    liste_groupes = []

    # Si la taille des groupes pour le brief est supérieur aux nombres d'apprenants on retourne un unique groupe de 
    # de tous les apprenants
    if brief_selec.nombre >= len(students):
        liste_groupes.append(students)
    # Si l a taille des groupes pour le brief est plus grand que la moitié du nombre d'apprenants, on retourne 2 groupes 
    # taille plus ou moins équivalente (on exclus les cas pour un nombre d'apprenant <= 3)
    elif brief_selec.nombre >= len(students)/2 and brief_selec.nombre < len(students) and  len(students) > 3:
        for i in range(len(students)//2):
            student = random.choice(students)
            res.append(student)
            students.remove(student)
        liste_groupes.append(res)
        liste_groupes.append([student for student in students])
    else :
        # S'il existe un reste pour la division euclidienne du nombre d'apprenant par la taille des n-omes, on extrait 
        # au hasard un nombre d'apprenant équivalent au reste
        if len(students) % brief_selec.nombre != 0:
            reste = len(students) % brief_selec.nombre
            while reste > 0 :
                random.shuffle(students)
                res.append(students.pop())
                reste -= 1
        # On crée les groupes sur la liste des apprenants restant au hasard
        while len(students) > 0 :
            count = 0
            group = []
            while count < brief_selec.nombre :
                random.shuffle(students)
                group.append(students.pop())
                count += 1
            liste_groupes.append(group)
        # Si la liste res est pas vide 
        if len(res) != 0 :
            # On vérifie que la taille de cette liste soit inférieur de 1 à la taille des n-omes et 
            #  si oui, on injecte ce reste d'apprenants en tant que groupe
            if len(res) == (len(liste_groupes[0]) - 1) and (len(liste_groupes[0]) >= 3):
                liste_groupes.append(res)
            # Si non, on insère les apprenants restants dans les autres groupes au hasard
            else:
                while len(res) > 0:
                    id = []
                    index_res = random.randrange(len(liste_groupes))
                    if index_res not in id:
                        id.append(index_res)
                        liste_groupes[index_res].append(res.pop())

    # On crée les objets Groupes et on indique les objets Apprenants qui correspondent au groupe
    for group in liste_groupes :  
        groupe_nom = '_'.join(x.prenom for x in group)
        django_groupe = Groupe(nom = groupe_nom,  brief = brief_selec)
        django_groupe.save()
        for i in group :
            django_groupe.apprenants.add(i)
import random

from .models import Apprenant, Brief, Groupe
from django.shortcuts import get_object_or_404, get_list_or_404



def groupe_create(brief_id):
    # Récupération de l'ensembles des apprenants
    students = get_list_or_404(Apprenant)
    brief_selec = get_object_or_404(Brief, pk = brief_id)
    
    res = []
    liste_groupes = []

    if brief_selec.nombre >= len(students):
        liste_groupes.append(students)
    elif brief_selec.nombre >= len(students)/2 and brief_selec.nombre < len(students):
        for i in range(len(students)//2):
            student = random.choice(students)
            res.append(student)
            students.remove(student)
        liste_groupes.append(res)
        liste_groupes.append([student for student in students])
    else :
        if len(students) % brief_selec.nombre != 0:
            reste = len(students) % brief_selec.nombre
            while reste > 0 :
                random.shuffle(students)
                res.append(students.pop())
                reste -= 1
        
        while len(students) > 0 :
            count = 0
            group = []
            while count < brief_selec.nombre :
                random.shuffle(students)
                group.append(students.pop())
                count += 1
            liste_groupes.append(group)
        
        if len(res) != 0 :
            if len(res) == (len(liste_groupes[0]) - 1) and (len(liste_groupes[0]) >= 3):
                liste_groupes.append(res)
            else:
                while len(res) > 0:
                    id = []
                    index_res = random.randrange(len(liste_groupes))
                    if index_res not in id:
                        id.append(index_res)
                        liste_groupes[index_res].append(res.pop())

    for group in liste_groupes :  
        groupe_nom = '_'.join(x.prenom for x in group)
        django_groupe = Groupe(nom = groupe_nom,  brief = brief_selec)
        django_groupe.save()
        for i in group :
            django_groupe.apprenants.add(i)
import random

from .models import Apprenant, Brief, Groupe



def groupe_create(brief_id):
    # Récupération de l'ensembles des apprenants
    students = list(Apprenant.objects.all())
    brief_selec = Brief.objects.get(pk = brief_id) 
    
    res = []
    liste_groupes = []
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
        django_groupe = Groupe(nom = groupe_nom,  brief = brief_selec )
        django_groupe.save()
        for i in group :
            django_groupe.apprenants.add(i)
        



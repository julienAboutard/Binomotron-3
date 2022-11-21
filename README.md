# Binomotron 3 - README  
  
## But du projet  

Dans ce projet nous avons réalisé un site internet, à l'aide de l'ORM de Django.

En nous appuyant sur un shcéma relationnel nous avons créé les tables de notre base de données : Apprenant, Groupe, Brief. Nous avons relié ses tables à l'aide des outils proposés par Django en utilisant des foreignKeys ainsi que des relations ManyToMany entre les tables Brief et Apprenant notamment. 
Le document binomotron/models.py établit les modèles de ces trois classes.

Nous avons modifié le fichier binomotron/settings.py en y insérant la ligne 'binomotron.apps.BinomotronConfig' dans INSTALLED_APPS. Nous avons aussi déclaré un utilisateur ayant accés à la base de données :

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'binomotron',
        'HOST':"localhost",
        'USER':"audrey",
        'PASSWORD':"root",
        'TEST': {
            'NAME': 'test_binomotron',
        },
    }
}
et nous avons changé la langue de notre projet en français.


Notre site est constitué de plusieurs pages HTML qui s'appuient toutes sur des Views Django (ces pages sont stockées dans le dossier 'templates' dans les sous-dossiers 'apprenant', 'brief' et 'other'):
- une page d'accueil 'index.html' qui nous permet d'accéder aux différents chemin de navigation de notre site internet
- des pages 'brief.html' et 'apprenant.html' accéssibles depuis l'accueil et qui permettent d'afficher respectivement les listes de briefs et apprenants disponibles dans notre base de données. Ces pages respectent la fonction de lecture de la base de données du CRUD. Il est possible directement depuis ces pages de créer (ajouter) des éléments dans notre base de données, de les modifier et de les supprimer (méthodes C, U et D du CRUD). 
Pour cela l'utilisateur est rediriger vers les templates respectifs : brief_add.html et apprenant_add.html, brief_edit.html et apprenant_edit.html, ainsi que brief_delete.html et apprenant_delete.html. 
Toutes ces pages suivent des chemins (paths) déterminés dans le fichier urls.py dans le dossier 'binomotron'.

Un des objectifs principaux de cette application est de proposer à l'utilisateur de générer des groupes aléatoires pour les briefs en fonction du nombre de personne par groupe exigées dans les données du brief. Pour cela nous avons associé un fichier group_crea.py qui génère les groupes. Cette application est accéssible dans la page de détail d'un groupe grâce à un bouton qui propose de créer les groupes s'ils n'existent pas déjà. 
Il n'est pas possible de supprimer les groupes créés, par contre si l'on modifie le nombre d'apprenants par groupe exigé dans le brief les groupes seront automatiquement supprimés et l'utilisateur devra refaire la démarche de création.

## Arborescense GitLab  
- Dossier sitebinomotron (Api créer avec Django)  
- fichier .gitignore  
- README.md  
- requirement.txt  (ensemble des packages pour faire tourner le projet)

## Collaborateurs  
- Audrey Costes
- Dorine Paris  
- Julien Aboutard  
- Vincent Boettcher  
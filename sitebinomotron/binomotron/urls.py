from django.urls import path

from . import views

app_name = 'binomotron'

urlpatterns = [

    path('', views.index, name='index'),

    path('apprenant/', views.apprenantview, name='apprenant'),
    path('apprenant/add/', views.ApprenantAddClass.as_view(), name = 'apprenant_add'),
    path('apprenant/edit/<int:pk>/', views.ApprenantEditClass.as_view(), name = 'apprenant_edit'),
    path('apprenant/<int:pk>/', views.ApprenantDetailView.as_view(), name='apprenant_detail'),
    path('apprenant/supprimer/<pk>/', views.ApprenantDeleteView.as_view(), name="supprimer-apprenant"),

    path('brief/', views.briefview, name='brief'),
    path('brief/add/', views.BriefAddClass.as_view(), name = 'brief_add'),
    path('brief/edit/<int:pk>/', views.BriefEditClass.as_view(), name = 'brief_edit'),
    path('brief/<int:pk>/', views.BriefDetailView.as_view(), name='brief_detail'),
    path('brief/supprimer/<pk>/', views.BriefDeleteView.as_view(), name="supprimer-brief"),

    path('groupe/create/<int:pk>', views.groupecreate , name ='groupe_create')


]
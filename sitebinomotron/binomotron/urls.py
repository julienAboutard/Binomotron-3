from django.urls import path

from . import views

app_name = 'binomotron'

urlpatterns = [
    # path('', views.IndexView.as_view(), name='index'),
    # path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # path('<int:question_id>/vote/', views.vote, name='vote'),

    path('', views.index, name='index'),
    path('apprenant/', views.ApprenantView.as_view(), name='apprenant'),
    path('apprenant/<int:pk>/', views.ApprenantDetailView.as_view(), name='detail'),


]
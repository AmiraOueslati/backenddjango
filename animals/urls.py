from django.urls import path
from .views import AnimalListCreateView, AnimalHistoryView
from animals import views
from .views import animal_list


urlpatterns = [
    path('', views.AnimalListCreateView.as_view(), name='animal-list-create'),  # Liste des animaux et ajout
    path('<int:pk>/history/', views.AnimalHistoryView.as_view(), name='animal-history'),  # Historique d'un animal
    path('add/', views.add_animal, name='add_animal'),  # Formulaire pour ajouter un animal
    path('list/', views.animal_list, name='animal_list'),  # Liste des animaux
]
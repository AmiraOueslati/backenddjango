from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Animal, GPSData
from animals.serializers import AnimalSerializer


# Liste et création des animaux
class AnimalListCreateView(APIView):
    def post(self, request):
        serializer = AnimalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        animals = Animal.objects.all()
        serializer = AnimalSerializer(animals, many=True)
        return Response(serializer.data)

# Historique GPS d'un animal
class AnimalHistoryView(APIView):
    def get(self, request, pk):
        try:
            animal = Animal.objects.get(pk=pk)
            gps_history = animal.gps_data.order_by('timestamp')  # Trier par timestamp
            data = [
                {
                    "latitude": gps.latitude,
                    "longitude": gps.longitude,
                    "timestamp": gps.timestamp.isoformat()
                }
                for gps in gps_history
            ]
            return Response({"history": data}, status=status.HTTP_200_OK)
        except Animal.DoesNotExist:
            return Response({"detail": "Animal not found."}, status=status.HTTP_404_NOT_FOUND)
from django.shortcuts import render, redirect
from .forms import AnimalForm

from django.shortcuts import render, redirect
from .forms import AnimalForm

def add_animal(request):
    if request.method == 'POST':
        form = AnimalForm(request.POST, request.FILES)  # Inclut les fichiers envoyés
        if form.is_valid():
            form.save()  # Enregistre l'animal dans la base de données
            return redirect('animal_list')  # Redirige vers la liste des animaux après ajout
    else:
        form = AnimalForm()  # Formulaire vide pour un GET
    return render(request, 'animals/add_animal.html', {'form': form})
from .models import Animal

def animal_list(request):
    animals = Animal.objects.all()  # Récupère tous les animaux
    return render(request, 'animals/animal_list.html', {'animals': animals})


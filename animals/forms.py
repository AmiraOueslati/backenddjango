from django import forms
from .models import Animal

class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ['name', 'latitude', 'longitude', 'description', 'start_time', 'end_time', 'image']
    
    # Si vous voulez personnaliser davantage le formulaire, vous pouvez ajouter un champ spécifique pour 'description'
    description = forms.ChoiceField(choices=Animal.ANIMAL_CHOICES)

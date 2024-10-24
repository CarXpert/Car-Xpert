from django import forms
from .models import Car  

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['brand', 'model', 'year', 'price_cash']  # Add other fields as needed

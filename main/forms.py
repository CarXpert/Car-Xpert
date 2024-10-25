# forms.py in the main app
from django import forms
from cars.models import Car  # Ensure you're importing the Car model from the correct app

class CarEditForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['model', 'color', 'year', 'fuel_type', 'cylinder_size', 'mileage', 
                  'stnk_date', 'levy_date', 'license_plate', 'price_cash', 'price_credit']
        
        widgets = {
            'stnk_date': forms.DateInput(attrs={'type': 'date'}),
            'levy_date': forms.DateInput(attrs={'type': 'date'}),
        }

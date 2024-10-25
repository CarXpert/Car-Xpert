# forms.py
from django import forms
from .models import Car

class CarEditForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['model', 'color', 'year', 'fuel_type', 'cylinder_size', 'mileage', 'stnk_date', 'levy_date', 'license_plate', 'price_cash', 'price_credit']

        widgets = {
            'stnk_date': forms.DateInput(attrs={'type': 'date'}),
            'levy_date': forms.DateInput(attrs={'type': 'date'}),
        }

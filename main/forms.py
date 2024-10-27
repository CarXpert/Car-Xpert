# forms.py in the main app
from django import forms
from cars.models import Car

class CarEditForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['model', 'color', 'year', 'fuel_type', 'cylinder_size', 'mileage', 
                  'stnk_date', 'levy_date', 'license_plate', 'price_cash', 'price_credit']
        
        widgets = {
            'stnk_date': forms.DateInput(attrs={'type': 'date'}),
            'levy_date': forms.DateInput(attrs={'type': 'date'}),
        }


class AddCarForm(forms.ModelForm):
    showroom_name = forms.CharField()
    showroom_location = forms.CharField()
    showroom_regency = forms.CharField()

    class Meta:
        model = Car
        fields = ['brand', 'car_type', 'model', 'color', 'year', 'transmission', 'fuel_type',
                  'doors', 'cylinder_size', 'cylinder_total', 'turbo', 'mileage', 'license_plate',
                  'price_cash', 'price_credit', 'pkb_value', 'pkb_base', 'stnk_date', 'levy_date',
                  'swdkllj', 'total_levy']
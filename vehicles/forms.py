from django import forms
from .models import Vehicle

class VehiclesForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ["client", "reg_plate","brand","model","production_year"]
        widget = {
            "client": forms.Select(attrs={"class":"input"}),
            "reg_plate": forms.TextInput(attrs={"class":"input", "placeholder":"ABC-1234"}),
            "brand": forms.TextInput(attrs={"class":"input"}),
            "model": forms.TextInput(attrs={"class":"input"}),
            "production_year": forms.NumberInput(attrs={"class":"input"}),
        }
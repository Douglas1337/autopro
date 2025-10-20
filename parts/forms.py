from django import forms 
from .models import Part

class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = ["name", "internal_code", "fabrication_code", "brand", "in_stock", "unit_price"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "input", "placeholder": "Fullname"}),
            "internal_code": forms.TextInput(attrs={"class": "input", "placeholder": "Internal usage code"}),
            "fabrication_code": forms.TextInput(attrs={"class": "input", "placeholder": "Part code"}),
            "brand": forms.TextInput(attrs={"class": "input", "placeholder": "Brand name"}),
            "in_stock": forms.NumberInput(attrs={"class": "input", "placeholder": "Quantity in stock"}),
            "unit_price": forms.NumberInput(attrs={"class": "input", "step": "0.01", "placeholder": "Part Price"}),
        }
from django import forms
from .models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["name", "phone", "email", "cpf_cnpj", "address"]  # <-- liste os campos
        widgets = {
            "name": forms.TextInput(attrs={"class": "input", "placeholder": "Nome completo"}),
            "phone": forms.TextInput(attrs={"class": "input", "placeholder": "(xx) xxxxx-xxxx"}),
            "email": forms.EmailInput(attrs={"class": "input", "placeholder": "email@dominio.com"}),
            "cpf_cnpj": forms.TextInput(attrs={"class": "input", "placeholder": "CPF ou CNPJ"}),
            "address": forms.TextInput(attrs={"class": "input", "placeholder": "Endereço"}),
        }
from django import forms
from .models import ServiceOrder

class ServiceOrderForm(forms.ModelForm):
    class Meta:
        model = ServiceOrder
        fields = [
            "client",
            "vehicle",
            "parts",
            "description",
            "notes",
            "status",
            "labor_cost",
            "expected_finish_date",
        ]

        widgets = {
            "client": forms.Select(attrs={"class": "input"}),
            "vehicle": forms.Select(attrs={"class": "input"}),
            "parts": forms.SelectMultiple(attrs={"class": "input"}),
            "problem_description": forms.Textarea(attrs={"class": "input", "rows": 4}),
            "notes": forms.Textarea(attrs={"class": "input", "rows": 3}),
            "status": forms.Select(attrs={"class": "input"}),
            "labor_cost": forms.NumberInput(attrs={"class": "input", "step": "0.01"}),
            "expected_finish_date": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "input"}
            ),
        }
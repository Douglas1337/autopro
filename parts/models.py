from django import forms
from django.db import models

# Create your models here.
class Part(models.Model):
    name = models.CharField(max_length=200)
    internal_code = models.CharField(max_length=200)
    fabrication_code = models.CharField(max_length=200)
    brand = models.CharField(max_length=50)
    in_stock = models.IntegerField()
    unit_price = models.DecimalField(decimal_places=2, max_digits=10)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ["name"]

    
    def __str__(self):
        return f"{self.name} {self.internal_code} ({self.unit_price})"
from django.db import models

# Create your models here.


from django.db import models
from clients.models import Client

class Vehicle(models.Model):
    reg_plate = models.CharField(max_length=10, unique=True)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    production_year = models.IntegerField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='vehicle')
    created_at = models.DateField(auto_now=True)
   

    def __str__(self):
        return f"{self.brand} {self.model} ({self.reg_plate})"

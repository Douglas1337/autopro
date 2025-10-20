from django.db import models

from clients.models import Client
from parts.models import Part
from vehicles.models import Vehicle


# Create your models here.
class ServiceOrder(models.Model):
    STATUS_CHOICES = [
        ("open", "Open"),
        ("in_progress", "In progress"),
        ("completed","Completed"),
        ("finished", "finished"),
    ]
    client = models.ForeignKey(Client,on_delete=models.CASCADE, related_name="service_orders")
    vehicle = models.ForeignKey(Vehicle,on_delete=models.CASCADE, related_name="service_orders")
    parts = models.ManyToManyField(Part, blank=True, related_name="service_orders")
    description = models.TextField("Problem description", blank=True, null=True)
    notes = models.TextField("Observations", blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Aberta")
    labor_cost = models.DecimalField("Labor Cost", max_digits=10, decimal_places=2, default=0)
    total_value = models.DecimalField("Total Value", max_digits=10, decimal_places=2, default=0)
    open_date = models.DateTimeField(auto_now_add=True)
    expected_finish_date = models.DateTimeField("Expected Finish Date", blank=True, null=True)
    close_date = models.DateTimeField("Close Date", blank=True, null=True)

    class Meta:
        ordering = ["-open_date"]

    def __str__(self):
        return f"Service Order #{self.id} - {self.client.name} ({self.vehicle.reg_plate})"
    
    def calculate_total (self):
        """ Sum of all parts of labor cost"""
        total_parts  = sum (p.unit_price for p in self.parts.all())
        self.total_value = total_parts + self.labor_cost
        return self.total_value
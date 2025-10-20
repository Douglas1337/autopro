from django.db import models

# Create your models here.

class Client(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    cpf_cnpj = models.CharField(max_length=20, unique=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.name} - {self.cpf_cnpj}"

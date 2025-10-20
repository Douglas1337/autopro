# 🧰 autoPRO – ERP for Mechanical Workshops

A management system (ERP) for mechanical workshops built with **Django**, supporting clients, vehicles, parts, and service orders.

---

## 🧱 1. Stack and Technologies

- **Backend**: Django 5.x (Python 3.12+)
- **Database**: PostgreSQL (via Docker)
- **Frontend**: Django Templates + CSS
- **Dependency management**: venv
- **Optional AI**: Ollama (for local diagnostic assistance)

---

## 🐘 2. Database (PostgreSQL via Docker)

Run PostgreSQL using Docker:

```bash
docker run -d   --name autoprodatabase   -e POSTGRES_DB=autopro_db   -e POSTGRES_USER=autopro   -e POSTGRES_PASSWORD=autopro   -p 5432:5432   postgres:16
```

Ensure it starts with the VM:
```bash
docker update --restart=always autoprodatabase
```

---

## 🧬 3. Django Project Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install django psycopg2-binary python-dotenv

django-admin startproject autopro
cd autopro
python manage.py startapp pages
python manage.py startapp clients
python manage.py startapp vehicles
python manage.py startapp parts
python manage.py startapp service_order
```

---

## ⚙️ 4. Database Configuration (`settings.py`)

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'autopro_db',
        'USER': 'autopro',
        'PASSWORD': 'autopro',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## 🧩 5. Pages App (Base and Landing Page)

`pages/views.py`

```python
from django.shortcuts import render

def home(request):
    return render(request, 'pages/home.html')
```

---

## 🎨 6. Base Template and CSS

`pages/templates/base.html`

```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{% block title %}autoPRO{% endblock %}</title>
  <link rel="stylesheet" href="{% static 'pages/css/style.css' %}">
</head>
<body>
  <header class="topbar">
    <div class="container">
      <a href="{% url 'pages:home' %}" class="brand">autoPRO</a>
      <nav class="nav">
        <a href="{% url 'clients:list' %}">Clients</a>
        <a href="{% url 'vehicles:list' %}">Vehicles</a>
        <a href="{% url 'parts:list' %}">Parts</a>
        <a href="{% url 'service_order:list' %}">Service Orders</a>
      </nav>
    </div>
  </header>
  <main class="container">
    {% if messages %}
      {% for message in messages %}
        <div class="message">{{ message }}</div>
      {% endfor %}
    {% endif %}
    {% block content %}{% endblock %}
  </main>
</body>
</html>
```

---

## 👥 7. Clients App

Manages customer registration.

`clients/models.py`
```python
from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    cpf_cnpj = models.CharField(max_length=20, unique=True)
    address = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
```

---

## 🚗 8. Vehicles App

`vehicles/models.py`
```python
from django.db import models
from clients.models import Client

class Vehicle(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="vehicles")
    plate = models.CharField(max_length=10, unique=True)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()

    class Meta:
        ordering = ["plate"]

    def __str__(self):
        return f"{self.plate} - {self.brand} {self.model}"
```

---

## ⚙️ 9. Parts App

`parts/models.py`
```python
from django.db import models

class Part(models.Model):
    name = models.CharField(max_length=200)
    internal_code = models.CharField(max_length=200)
    fabrication_code = models.CharField(max_length=200)
    brand = models.CharField(max_length=50)
    in_stock = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} [{self.internal_code}]"
```

---

## 🧾 10. Service Orders App

`service_order/models.py`
```python
from django.db import models
from clients.models import Client
from vehicles.models import Vehicle
from parts.models import Part

class ServiceOrder(models.Model):
    STATUS_CHOICES = [
        ("open", "Open"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="service_orders")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="service_orders")
    parts = models.ManyToManyField(Part, blank=True, related_name="service_orders")

    problem_description = models.TextField()
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")
    labor_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    open_date = models.DateTimeField(auto_now_add=True)
    expected_finish_date = models.DateTimeField(blank=True, null=True)
    close_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-open_date"]

    def __str__(self):
        return f"Order #{self.id} - {self.client.name}"

    def calculate_total(self):
        total_parts = sum(p.unit_price for p in self.parts.all())
        self.total_value = total_parts + self.labor_cost
        return self.total_value
```

---

## 🧮 11. Automatic Stock Update

`service_order/signals.py`
```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ServiceOrder

@receiver(post_save, sender=ServiceOrder)
def update_stock_on_completion(sender, instance, created, **kwargs):
    if created:
        return
    if instance.status == "completed":
        for part in instance.parts.all():
            if part.in_stock > 0:
                part.in_stock -= 1
                part.save()
```

`service_order/apps.py`
```python
from django.apps import AppConfig

class ServiceOrderConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "service_order"

    def ready(self):
        import service_order.signals
```

---

## 🧭 12. Main URLs

`autopro/urls.py`
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("pages.urls")),
    path("clients/", include("clients.urls")),
    path("vehicles/", include("vehicles.urls")),
    path("parts/", include("parts.urls")),
    path("os/", include("service_order.urls")),
]
```

---

## 🧰 13. Migrations and Run

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Access:
- `/` → Home
- `/clients/` → Clients
- `/vehicles/` → Vehicles
- `/parts/` → Parts
- `/os/` → Service Orders

---

## ✅ 14. Next Steps

| Feature | Description |
|----------|--------------|
| 📊 Reports | View orders by status or client |
| 📦 Stock control | Add quantity used per part |
| 🔐 Authentication | Add user login and permissions |
| 🧾 PDF export | Generate printable OS documents |
| 🤖 AI Integration | Suggest diagnostics using local Ollama |

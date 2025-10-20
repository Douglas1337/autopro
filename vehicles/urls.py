from django.urls import path
from . import views

app_name = "vehicles"
urlpatterns = [
    path("",views.VehicleListViews.as_view(), name="list"),
    path("new/", views.VehicleCreateView.as_view(), name="create"),
    path("<int:pk>/edit/", views.VehicleUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", views.VehicleDeleteView.as_view(), name="delete"),
]
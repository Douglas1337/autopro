from django.urls import path
from . import views

app_name = "parts"
urlpatterns = [
    path("", views.PartListView.as_view(), name="list"),
    path("new/", views.PartCreateView.as_view(), name="create"),
    path("<int:pk>/edit/", views.PartUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", views.PartUpdateView.as_view(), name="delete"),
]

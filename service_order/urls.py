from django.urls import path
from . import views

app_name = "service_order"
urlpatterns = [
    path("", views.ServiceOrderListView.as_view(), name="list"),
    path("new/", views.ServiceOrderCreateView.as_view(), name="create"),
    path("<int:pk>/edit/", views.ServiceOrderUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", views.ServiceOrderDeleteView.as_view(), name="delete")
]

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Vehicle
from .forms import VehiclesForm


class VehicleListViews(ListView):
    model = Vehicle
    template_name = "vehicles/list.html"
    context_object_name = "vehicles"
    paginate_by = 10
    ordering = ["reg_plate"]

    def get_queryset(self):    
        qs = super().get_queryset().select_related("client")
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(reg_plate_icontains=q) | qs.filter(brand_icontains=q) | qs.filter(model_icontains=q)
        return qs
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q","").strip()
        return ctx
    
class VehicleCreateView(SuccessMessageMixin, CreateView):
    model = Vehicle
    form_class = VehiclesForm
    template_name = "vehicles/form.html"
    success_url = reverse_lazy("vehicles:list")
    success_message = "Vehicle successfully added."

class VehicleUpdateView(SuccessMessageMixin, UpdateView):
    model = Vehicle
    form_class = VehiclesForm
    template_name = "vehicles/form.html"
    success_url = reverse_lazy("vehicles:list")
    success_message = "Vehicle successfully updated." 

class VehicleDeleteView(SuccessMessageMixin, DeleteView):
    model = Vehicle
    form_class = VehiclesForm
    template_name = "vehicles/confirm_delete.html"
    success_url = reverse_lazy("vehicles:list")
    

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Vehicle successfully removed.")
        return super().delete(request, *args, **kwargs)
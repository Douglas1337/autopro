from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import ServiceOrder
from .forms import ServiceOrderForm

class ServiceOrderListView(ListView):
    model = ServiceOrder
    template_name = "service_order/list.html"
    context_object_name = "orders"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related("client", "vehicle").prefetch_related("parts")
        q = self.request.GET.get("q", "").strip()
        status = self.request.GET.get("status", "")
        if q:
            qs = qs.filter(client_nameicontains=q) | qs.filter(vehicleplate_icontains=q)
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "").strip()
        ctx["status"] = self.request.GET.get("status", "")
        ctx["status_choices"] = ServiceOrder.STATUS_CHOICES
        return ctx


class ServiceOrderCreateView(SuccessMessageMixin, CreateView):
    model = ServiceOrder
    form_class = ServiceOrderForm
    template_name = "service_order/form.html"
    success_url = reverse_lazy("service_order:list")
    success_message = "Service order created successfully."

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.calculate_total()
        self.object.save()
        return response


class ServiceOrderUpdateView(SuccessMessageMixin, UpdateView):
    model = ServiceOrder
    form_class = ServiceOrderForm
    template_name = "service_order/form.html"
    success_url = reverse_lazy("service_order:list")
    success_message = "Service order updated successfully."

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.calculate_total()
        self.object.save()
        return response


class ServiceOrderDeleteView(DeleteView):
    model = ServiceOrder
    template_name = "service_order/confirm_delete.html"
    success_url = reverse_lazy("service_order:list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Service order deleted successfully.")
        return super().delete(request, *args, **kwargs)
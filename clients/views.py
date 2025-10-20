from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Client
from .forms import ClientForm

class ClientListView(ListView):
    model = Client
    template_name = "clients/list.html"
    context_object_name = "clients"
    paginate_by = 10
    ordering = ["name"]

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(name__icontains=q) | qs.filter(cpf_cnpj__icontains=q) | qs.filter(email__icontains=q)
        return qs


    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "").strip()
        return ctx


class ClientCreateView(SuccessMessageMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = "clients/form.html"
    success_url = reverse_lazy("clients:list")
    success_message = "Cliente criado com sucesso."

class ClientUpdateView(SuccessMessageMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "clients/form.html"
    success_url = reverse_lazy("clients:list")
    success_message = "Cliente atualizado com sucesso."

class ClientDeleteView(DeleteView):
    model = Client
    template_name = "clients/confirm_delete.html"
    success_url = reverse_lazy("clients:list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Cliente removido com sucesso.")
        return super().delete(request, *args, **kwargs)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Part
from .forms import PartForm

class PartListView(ListView):
    model = Part
    template_name = "parts/list.html"
    context_object_name = "parts"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(name_icontains=q) | qs.filter(internal_codeicontains=q) | qs.filter(fabrication_code_icontains=q)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "").strip()
        return ctx

class PartCreateView(SuccessMessageMixin, CreateView):
    model = Part
    form_class = PartForm
    template_name = "parts/form.html"
    success_url = reverse_lazy("parts:list")
    success_message = "Part successfully added."

class PartUpdateView(SuccessMessageMixin, UpdateView):
    model = Part
    form_class = PartForm
    template_name = "parts/form.html"
    success_url = reverse_lazy("parts:list")
    success_message = "Part successfuly updated."

class PartDeleteView(DeleteView):
    model = Part
    template_name = "parts/confirm_delete.html"
    success_url = reverse_lazy("parts:list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Part successfully deleted.")
        return super().delete(request, *args, **kwargs)
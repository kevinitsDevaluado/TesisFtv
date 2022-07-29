import json

from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.clinic.forms import BreedPet, BreedPetForm
from core.security.mixins import PermissionMixin


class BreedPetListView(PermissionMixin, ListView):
    model = BreedPet
    template_name = 'breedpet/list.html'
    permission_required = 'view_breedpet'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('breedpet_create')
        context['title'] = 'Listado de Tipos de Razas de Animales'
        return context


class BreedPetCreateView(PermissionMixin, CreateView):
    model = BreedPet
    template_name = 'breedpet/create.html'
    form_class = BreedPetForm
    success_url = reverse_lazy('breedpet_list')
    permission_required = 'add_breedpet'

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            name = self.request.POST['name'].strip()
            if len(type):
                if BreedPet.objects.filter(name__iexact=name, type_id=type):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de un Tipo de Raza de Animal'
        context['action'] = 'add'
        return context


class BreedPetUpdateView(PermissionMixin, UpdateView):
    model = BreedPet
    template_name = 'breedpet/create.html'
    form_class = BreedPetForm
    success_url = reverse_lazy('breedpet_list')
    permission_required = 'change_breedpet'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def validate_data(self):
        data = {'valid': True}
        try:
            id = self.get_object().id
            type = self.request.POST['type']
            name = self.request.POST['name'].strip()
            if len(type):
                if BreedPet.objects.filter(name__iexact=name, type_id=type).exclude(id=id):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                data = self.get_form().save()
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de un Tipo de Raza de Animal'
        context['action'] = 'edit'
        return context


class BreedPetDeleteView(PermissionMixin, DeleteView):
    model = BreedPet
    template_name = 'breedpet/delete.html'
    success_url = reverse_lazy('breedpet_list')
    permission_required = 'delete_breedpet'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.get_object().delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context

import json

from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.clinic.forms import TypePet, TypePetForm
from core.security.mixins import PermissionMixin


class TypePetListView(PermissionMixin, ListView):
    model = TypePet
    template_name = 'typepet/list.html'
    permission_required = 'view_typepet'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('typepet_create')
        context['title'] = 'Listado de Tipos de Animales'
        return context


class TypePetCreateView(PermissionMixin, CreateView):
    model = TypePet
    template_name = 'typepet/create.html'
    form_class = TypePetForm
    success_url = reverse_lazy('typepet_list')
    permission_required = 'add_typepet'

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            if type == 'name':
                if TypePet.objects.filter(name__iexact=obj):
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
        context['title'] = 'Nuevo registro de un Tipo de Animal'
        context['action'] = 'add'
        return context


class TypePetUpdateView(PermissionMixin, UpdateView):
    model = TypePet
    template_name = 'typepet/create.html'
    form_class = TypePetForm
    success_url = reverse_lazy('typepet_list')
    permission_required = 'change_typepet'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            id = self.get_object().id
            if type == 'name':
                if TypePet.objects.filter(name__iexact=obj).exclude(id=id):
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
        context['title'] = 'Edición de un Tipo de Animal'
        context['action'] = 'edit'
        return context


class TypePetDeleteView(PermissionMixin, DeleteView):
    model = TypePet
    template_name = 'typepet/delete.html'
    success_url = reverse_lazy('typepet_list')
    permission_required = 'delete_typepet'

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

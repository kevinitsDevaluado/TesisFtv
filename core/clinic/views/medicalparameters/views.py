import json

from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.clinic.forms import MedicalParameters, MedicalParametersForm
from core.security.mixins import PermissionMixin


class MedicalParametersListView(PermissionMixin, ListView):
    model = MedicalParameters
    template_name = 'medicalparameters/list.html'
    permission_required = 'view_medicalparameters'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('medicalparameters_create')
        context['title'] = 'Listado de Parámetros Médicos'
        return context


class MedicalParametersCreateView(PermissionMixin, CreateView):
    model = MedicalParameters
    template_name = 'medicalparameters/create.html'
    form_class = MedicalParametersForm
    success_url = reverse_lazy('medicalparameters_list')
    permission_required = 'add_medicalparameters'

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            if type == 'name':
                if MedicalParameters.objects.filter(name__iexact=obj):
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
        context['title'] = 'Nuevo registro de un Parámetro Médico'
        context['action'] = 'add'
        return context


class MedicalParametersUpdateView(PermissionMixin, UpdateView):
    model = MedicalParameters
    template_name = 'medicalparameters/create.html'
    form_class = MedicalParametersForm
    success_url = reverse_lazy('medicalparameters_list')
    permission_required = 'change_medicalparameters'

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
                if MedicalParameters.objects.filter(name__iexact=obj).exclude(id=id):
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
        context['title'] = 'Edición de un Parámetro Médico'
        context['action'] = 'edit'
        return context


class MedicalParametersDeleteView(PermissionMixin, DeleteView):
    model = MedicalParameters
    template_name = 'medicalparameters/delete.html'
    success_url = reverse_lazy('medicalparameters_list')
    permission_required = 'delete_medicalparameters'

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

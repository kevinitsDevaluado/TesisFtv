import json

from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.clinic.forms import Canton, CantonForm
from core.security.mixins import PermissionMixin


class CantonListView(PermissionMixin, ListView):
    model = Canton
    template_name = 'canton/list.html'
    permission_required = 'view_canton'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('canton_create')
        context['title'] = 'Listado de Cantones'
        return context


class CantonCreateView(PermissionMixin, CreateView):
    model = Canton
    template_name = 'canton/create.html'
    form_class = CantonForm
    success_url = reverse_lazy('canton_list')
    permission_required = 'add_canton'

    def validate_data(self):
        data = {'valid': True}
        try:
            name = self.request.POST['name'].strip()
            prov = self.request.POST['prov']
            if len(prov):
                if Canton.objects.filter(name__iexact=name, province_id=prov):
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
        context['title'] = 'Nuevo registro de un Cantón'
        context['action'] = 'add'
        return context


class CantonUpdateView(PermissionMixin, UpdateView):
    model = Canton
    template_name = 'canton/create.html'
    form_class = CantonForm
    success_url = reverse_lazy('canton_list')
    permission_required = 'change_canton'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def validate_data(self):
        data = {'valid': True}
        try:
            id = self.get_object().id
            name = self.request.POST['name'].strip()
            prov = self.request.POST['prov']
            if len(prov):
                if Canton.objects.filter(name__iexact=name, province_id=prov).exclude(id=id):
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
        context['title'] = 'Edición de un Cantón'
        context['action'] = 'edit'
        return context


class CantonDeleteView(PermissionMixin, DeleteView):
    model = Canton
    template_name = 'canton/delete.html'
    success_url = reverse_lazy('canton_list')
    permission_required = 'delete_canton'

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

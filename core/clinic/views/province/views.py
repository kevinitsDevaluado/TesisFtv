import json

from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.clinic.forms import Province, ProvinceForm
from core.security.mixins import PermissionMixin


class ProvinceListView(PermissionMixin, ListView):
    model = Province
    template_name = 'province/list.html'
    permission_required = 'view_province'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('province_create')
        context['title'] = 'Listado de Provincias'
        return context


class ProvinceCreateView(PermissionMixin, CreateView):
    model = Province
    template_name = 'province/create.html'
    form_class = ProvinceForm
    success_url = reverse_lazy('province_list')
    permission_required = 'add_province'

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            if type == 'name':
                if Province.objects.filter(name__iexact=obj):
                    data['valid'] = False
            elif type == 'code':
                if Province.objects.filter(code=obj):
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
        context['title'] = 'Nuevo registro de una Provincia'
        context['action'] = 'add'
        return context


class ProvinceUpdateView(PermissionMixin, UpdateView):
    model = Province
    template_name = 'province/create.html'
    form_class = ProvinceForm
    success_url = reverse_lazy('province_list')
    permission_required = 'change_province'

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
                if Province.objects.filter(name__iexact=obj).exclude(id=id):
                    data['valid'] = False
            elif type == 'code':
                if Province.objects.filter(code=obj).exclude(id=id):
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
        context['title'] = 'Edición de una Provincia'
        context['action'] = 'edit'
        return context


class ProvinceDeleteView(PermissionMixin, DeleteView):
    model = Province
    template_name = 'province/delete.html'
    success_url = reverse_lazy('province_list')
    permission_required = 'delete_province'

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

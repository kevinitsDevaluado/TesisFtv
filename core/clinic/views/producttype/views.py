import json

from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.clinic.forms import ProductTypeForm, ProductType
from core.security.mixins import PermissionMixin


class ProductTypeListView(PermissionMixin, ListView):
    model = ProductType
    template_name = 'producttype/list.html'
    permission_required = 'view_producttype'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('producttype_create')
        context['title'] = 'Listado de Tipos de Productos'
        return context


class ProductTypeCreateView(PermissionMixin, CreateView):
    model = ProductType
    template_name = 'producttype/create.html'
    form_class = ProductTypeForm
    success_url = reverse_lazy('producttype_list')
    permission_required = 'add_producttype'

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            if type == 'name':
                if ProductType.objects.filter(name__icontains=obj):
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
        context['title'] = 'Nuevo registro de un Tipo de Producto'
        context['action'] = 'add'
        return context


class ProductTypeUpdateView(PermissionMixin, UpdateView):
    model = ProductType
    template_name = 'producttype/create.html'
    form_class = ProductTypeForm
    success_url = reverse_lazy('producttype_list')
    permission_required = 'change_producttype'

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
                if ProductType.objects.filter(name__icontains=obj).exclude(id=id):
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
        context['title'] = 'Edición de un Tipo de Producto'
        context['action'] = 'edit'
        return context


class ProductTypeDeleteView(PermissionMixin, DeleteView):
    model = ProductType
    template_name = 'producttype/delete.html'
    success_url = reverse_lazy('producttype_list')
    permission_required = 'delete_producttype'

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


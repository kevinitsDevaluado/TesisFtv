import json

from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.clinic.forms import Parish, ParishForm
from core.security.mixins import PermissionMixin


class ParishListView(PermissionMixin, ListView):
    model = Parish
    template_name = 'parish/list.html'
    permission_required = 'view_parish'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                for i in Parish.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('parish_create')
        context['title'] = 'Listado de Parroquias'
        return context


class ParishCreateView(PermissionMixin, CreateView):
    model = Parish
    template_name = 'parish/create.html'
    form_class = ParishForm
    success_url = reverse_lazy('parish_list')
    permission_required = 'add_parish'

    def validate_data(self):
        data = {'valid': True}
        try:
            name = self.request.POST['name'].strip()
            canton = self.request.POST['canton']
            if len(canton):
                if Parish.objects.filter(name__iexact=name, canton_id=canton):
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
        context['title'] = 'Nuevo registro de una Parroquia'
        context['action'] = 'add'
        return context


class ParishUpdateView(PermissionMixin, UpdateView):
    model = Parish
    template_name = 'parish/create.html'
    form_class = ParishForm
    success_url = reverse_lazy('parish_list')
    permission_required = 'change_parish'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def validate_data(self):
        data = {'valid': True}
        try:
            id = self.get_object().id
            name = self.request.POST['name'].strip()
            canton = self.request.POST['canton']
            if len(canton):
                if Parish.objects.filter(name__iexact=name, canton_id=canton).exclude(id=id):
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
        context['title'] = 'Edición de una Parroquia'
        context['action'] = 'edit'
        return context


class ParishDeleteView(PermissionMixin, DeleteView):
    model = Parish
    template_name = 'parish/delete.html'
    success_url = reverse_lazy('parish_list')
    permission_required = 'delete_parish'

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

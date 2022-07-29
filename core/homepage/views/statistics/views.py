import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.homepage.forms import Statistics, StatisticsForm
from core.security.mixins import PermissionMixin


class StatisticsListView(PermissionMixin, ListView):
    model = Statistics
    template_name = 'statistics/list.html'
    permission_required = 'view_statistics'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('statistics_create')
        context['title'] = 'Listado de Estadísticas'
        return context


class StatisticsCreateView(PermissionMixin, CreateView):
    model = Statistics
    template_name = 'statistics/create.html'
    form_class = StatisticsForm
    success_url = reverse_lazy('statistics_list')
    permission_required = 'add_statistics'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de una Estadística'
        context['action'] = 'add'
        return context


class StatisticsUpdateView(PermissionMixin, UpdateView):
    model = Statistics
    template_name = 'statistics/create.html'
    form_class = StatisticsForm
    success_url = reverse_lazy('statistics_list')
    permission_required = 'change_statistics'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                data = self.get_form().save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de una Estadística'
        context['action'] = 'edit'
        return context


class StatisticsDeleteView(PermissionMixin, DeleteView):
    model = Statistics
    template_name = 'statistics/delete.html'
    success_url = reverse_lazy('statistics_list')
    permission_required = 'delete_statistics'

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

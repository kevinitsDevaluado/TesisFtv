import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.homepage.forms import Team, TeamForm
from core.security.mixins import PermissionMixin


class TeamListView(PermissionMixin, ListView):
    model = Team
    template_name = 'mecanicos/list.html'
    permission_required = 'view_team'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('team_create')
        context['title'] = 'Listado de Equipo de Trabajo'
        return context


class TeamCreateView(PermissionMixin, CreateView):
    model = Team
    template_name = 'mecanicos/create.html'
    form_class = TeamForm
    success_url = reverse_lazy('team_list')
    permission_required = 'add_team'

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
        context['title'] = 'Nuevo registro de un Empleado'
        context['action'] = 'add'
        return context


class TeamUpdateView(PermissionMixin, UpdateView):
    model = Team
    template_name = 'mecanicos/create.html'
    form_class = TeamForm
    success_url = reverse_lazy('team_list')
    permission_required = 'change_team'

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
        context['title'] = 'Edición de un Empleado'
        context['action'] = 'edit'
        return context


class TeamDeleteView(PermissionMixin, DeleteView):
    model = Team
    template_name = 'mecanicos/delete.html'
    success_url = reverse_lazy('team_list')
    permission_required = 'delete_team'

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

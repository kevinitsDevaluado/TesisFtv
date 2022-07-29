import json

from django.db import transaction
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.homepage.forms import Team, TeamForm, TeamSocialNet
from core.security.mixins import PermissionMixin


class TeamListView(PermissionMixin, ListView):
    model = Team
    template_name = 'team/list.html'
    permission_required = 'view_team'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('team_create')
        context['title'] = 'Listado de Doctores'
        return context


class TeamCreateView(PermissionMixin, CreateView):
    model = Team
    template_name = 'team/create.html'
    form_class = TeamForm
    success_url = reverse_lazy('team_list')
    permission_required = 'add_team'

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'add':
                with transaction.atomic():
                    team = Team()
                    s = request.POST.get('names')
                    print('trayendo ', s)
                    #team.names = request.POST['names']
                    #team.job = request.POST['job']
                    #team.desc = request.POST['desc']
                    #team.phrase = request.POST['phrase']
                    #team.state = 'state' in request.POST
                    #if 'image' in request.FILES:
                    #    team.image = request.FILES['image']
                    #team.save()
                    
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de un Doctor'
        context['action'] = 'add'
        context['social'] = []
        return context


class TeamUpdateView(PermissionMixin, UpdateView):
    model = Team
    template_name = 'team/create.html'
    form_class = TeamForm
    success_url = reverse_lazy('team_list')
    permission_required = 'change_team'

    def get_socialnet(self):
        data = []
        try:
            team = Team.objects.get(pk=self.kwargs['pk'])
            for i in team.teamsocialnet_set.all():
                data.append(i.toJSON())
        except:
            pass
        return data

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'edit':
                with transaction.atomic():
                    team = self.get_object()
                    team.names = request.POST['names']
                    team.job = request.POST['job']
                    team.desc = request.POST['desc']
                    team.phrase = request.POST['phrase']
                    team.state = 'state' in request.POST
                    if 'image' in request.FILES:
                        team.image = request.FILES['image']
                    team.save()
                    team.teamsocialnet_set.all().delete()
                    for s in json.loads(request.POST['socialnet']):
                        det = TeamSocialNet()
                        det.team = team
                        det.icon = s['icon']
                        det.name = s['name']
                        det.url = s['url']
                        det.save()
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de un Doctor'
        context['action'] = 'edit'
        context['social'] = json.dumps(self.get_socialnet())
        return context


class TeamDeleteView(PermissionMixin, DeleteView):
    model = Team
    template_name = 'team/delete.html'
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

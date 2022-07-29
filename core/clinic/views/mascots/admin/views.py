import json

from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, FormView

from core.clinic.forms import Mascots, MascotsForm, User, Client
from core.clinic.models import BreedPet
from core.security.mixins import PermissionMixin


class MascotsAdminListView(PermissionMixin, FormView):
    form_class = MascotsForm
    template_name = 'mascots/admin/list.html'
    permission_required = 'view_mascots_admin'

    def get_form(self, form_class=None):
        form = MascotsForm()
        form.fields['client'].queryset = Client.objects.filter()
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                client = request.POST['client']
                search = Mascots.objects.filter()
                if len(client):
                    search = search.filter(client_id=client)
                pos = 1
                for m in search.order_by('id'):
                    item = m.toJSON()
                    item['pos'] = pos
                    data.append(item)
                    pos += 1
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('mascots_admin_create')
        context['title'] = 'Listado de Vehículos'
        return context


class MascotsAdminCreateView(PermissionMixin, CreateView):
    model = Mascots
    template_name = 'mascots/admin/create.html'
    form_class = MascotsForm
    success_url = reverse_lazy('mascots_admin_list')
    permission_required = 'add_mascots_admin'

    def get_form(self, form_class=None):
        form = MascotsForm()
        form.fields['client'].queryset = User.objects.none()
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                mascot = Mascots()
                mascot.client_id = request.POST['client']
                mascot.name = request.POST['name']
                mascot.breed_id = 1
                mascot.color_id = 1
                mascot.gender = 1
                mascot.observation = request.POST['observation']
                if 'image' in request.FILES:
                    mascot.image = request.FILES['image']
                mascot.save()
            elif action == 'search_client':
                data = []
                term = request.POST['term']
                for i in Client.objects.filter(
                        Q(user__first_name__icontains=term) | Q(user__last_name__icontains=term) | Q(
                            user__dni__icontains=term))[0:10]:
                    item = {'id': i.id, 'text': '{} / {}'.format(i.user.get_full_name(), i.user.dni)}
                    data.append(item)
            elif action == 'search_breed':
                data = [{'id': '', 'text': '-------------'}]
                typepet = request.POST['typepet']
                if len(typepet):
                    for b in BreedPet.objects.filter(type_id=typepet):
                        data.append({
                            'id': b.id, 'text': b.name
                        })
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de un Vehículo'
        context['action'] = 'add'
        return context


class MascotsAdminUpdateView(PermissionMixin, UpdateView):
    model = Mascots
    template_name = 'mascots/admin/create.html'
    form_class = MascotsForm
    success_url = reverse_lazy('mascots_admin_list')
    permission_required = 'change_mascots_admin'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        instance = self.get_object()
        form = MascotsForm(instance=instance, initial={
            'typepet': instance.breed.type
        })
        form.fields['breed'].queryset = BreedPet.objects.filter(type=instance.breed.type)
        if instance.client:
            form.fields['client'].queryset = User.objects.filter(id=instance.client.id)
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                mascot = self.object
                mascot.client_id = request.POST['client']
                mascot.name = request.POST['name']
                mascot.breed_id = request.POST['breed']
                mascot.color_id = request.POST['color']
                mascot.birthdate = request.POST['birthdate']
                mascot.gender = request.POST['gender']
                mascot.observation = request.POST['observation']
                if 'image-clear' in request.POST:
                    mascot.remove_image()
                    mascot.image = None
                if 'image' in request.FILES:
                    mascot.image = request.FILES['image']
                mascot.save()
            elif action == 'search_client':
                data = []
                term = request.POST['term']
                for i in Client.objects.filter(
                        Q(user__first_name__icontains=term) | Q(user__last_name__icontains=term) | Q(
                            user__dni__icontains=term))[0:10]:
                    item = {'id': i.id, 'text': '{} / {}'.format(i.user.get_full_name(), i.dni)}
                    data.append(item)
            elif action == 'search_breed':
                data = [{'id': '', 'text': '-------------'}]
                typepet = request.POST['typepet']
                if len(typepet):
                    for b in BreedPet.objects.filter(type_id=typepet):
                        data.append({
                            'id': b.id, 'text': b.name
                        })
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de una Mascota'
        context['action'] = 'edit'
        return context


class MascotsAdminDeleteView(PermissionMixin, DeleteView):
    model = Mascots
    template_name = 'mascots/admin/delete.html'
    success_url = reverse_lazy('mascots_admin_list')
    permission_required = 'delete_mascots_admin'

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

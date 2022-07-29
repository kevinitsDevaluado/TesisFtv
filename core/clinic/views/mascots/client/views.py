import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, FormView

from core.clinic.forms import Mascots, MascotsForm
from core.clinic.models import BreedPet
from core.security.mixins import PermissionMixin


class MascotsClientListView(PermissionMixin, FormView):
    form_class = MascotsForm
    template_name = 'mascots/client/list.html'
    permission_required = 'view_mascots_client'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                pos = 1
                for m in Mascots.objects.filter(client_id=request.user.client.id).order_by('id'):
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
        context['create_url'] = reverse_lazy('mascots_client_create')
        context['title'] = 'Listado de Vehículos'
        return context


class MascotsClientCreateView(PermissionMixin, CreateView):
    model = Mascots
    template_name = 'mascots/client/create.html'
    form_class = MascotsForm
    success_url = reverse_lazy('mascots_client_list')
    permission_required = 'add_mascots_client'

    def get_form(self, form_class=None):
        form = MascotsForm()
        del form.fields['client']
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                mascot = Mascots()
                mascot.client_id = request.user.client.id
                mascot.color_id = request.POST['color']
                mascot.name = request.POST['name']
                if 'image' in request.FILES:
                    mascot.image = request.FILES['image']
                mascot.breed_id = request.POST['breed']
                mascot.gender = request.POST['gender']
                mascot.birthdate = request.POST['birthdate']
                mascot.observation = request.POST['observation']
                mascot.save()
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
        context['action'] = 'add'
        return context


class MascotsClientUpdateView(PermissionMixin, UpdateView):
    model = Mascots
    template_name = 'mascots/client/create.html'
    form_class = MascotsForm
    success_url = reverse_lazy('mascots_client_list')
    permission_required = 'change_mascots_client'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        instance = self.get_object()
        form = MascotsForm(instance=instance, initial={
            'typepet': instance.breed.type
        })
        form.fields['breed'].queryset = BreedPet.objects.filter(type=instance.breed.type)
        del form.fields['client']
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                mascot = self.object
                mascot.color_id = request.POST['color']
                mascot.name = request.POST['name']
                if 'image' in request.FILES:
                    mascot.image = request.FILES['image']
                if 'image-clear' in request.POST:
                    mascot.remove_image()
                    mascot.image = None
                mascot.breed_id = request.POST['breed']
                mascot.gender = request.POST['gender']
                mascot.birthdate = request.POST['birthdate']
                mascot.observation = request.POST['observation']
                mascot.save()
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
        context['title'] = 'Edición de una Mascota'
        context['action'] = 'edit'
        return context


class MascotsClientDeleteView(PermissionMixin, DeleteView):
    model = Mascots
    template_name = 'mascots/client/delete.html'
    success_url = reverse_lazy('mascots_client_list')
    permission_required = 'delete_mascots_client'

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

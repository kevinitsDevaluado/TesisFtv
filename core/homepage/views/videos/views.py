import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.homepage.forms import Videos, VideosForm
from core.security.mixins import PermissionMixin


class VideosListView(PermissionMixin, ListView):
    model = Videos
    template_name = 'videos/list.html'
    permission_required = 'view_videos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('videos_create')
        context['title'] = 'Listado de Videos'
        return context


class VideosCreateView(PermissionMixin, CreateView):
    model = Videos
    template_name = 'videos/create.html'
    form_class = VideosForm
    success_url = reverse_lazy('videos_list')
    permission_required = 'add_videos'

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
        context['title'] = 'Nuevo registro de un Video'
        context['action'] = 'add'
        return context


class VideosUpdateView(PermissionMixin, UpdateView):
    model = Videos
    template_name = 'videos/create.html'
    form_class = VideosForm
    success_url = reverse_lazy('videos_list')
    permission_required = 'change_videos'

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
        context['title'] = 'Edición de un Video'
        context['action'] = 'edit'
        return context


class VideosDeleteView(PermissionMixin, DeleteView):
    model = Videos
    template_name = 'videos/delete.html'
    success_url = reverse_lazy('videos_list')
    permission_required = 'delete_videos'

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

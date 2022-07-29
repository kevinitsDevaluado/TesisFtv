import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.homepage.forms import Gallery, GalleryForm
from core.security.mixins import PermissionMixin


class GalleryListView(PermissionMixin, ListView):
    model = Gallery
    template_name = 'gallery/list.html'
    permission_required = 'view_gallery'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('gallery_create')
        context['title'] = 'Listado de Imágenes'
        return context


class GalleryCreateView(PermissionMixin, CreateView):
    model = Gallery
    template_name = 'gallery/create.html'
    form_class = GalleryForm
    success_url = reverse_lazy('gallery_list')
    permission_required = 'add_gallery'

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
        context['title'] = 'Nuevo registro de una Imagen'
        context['action'] = 'add'
        return context


class GalleryUpdateView(PermissionMixin, UpdateView):
    model = Gallery
    template_name = 'gallery/create.html'
    form_class = GalleryForm
    success_url = reverse_lazy('gallery_list')
    permission_required = 'change_gallery'

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
        context['title'] = 'Edición de una Imagen'
        context['action'] = 'edit'
        return context


class GalleryDeleteView(PermissionMixin, DeleteView):
    model = Gallery
    template_name = 'gallery/delete.html'
    success_url = reverse_lazy('gallery_list')
    permission_required = 'delete_gallery'

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

import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.homepage.forms import FreqQuestions, FreqQuestionsForm
from core.security.mixins import PermissionMixin


class FreqQuestionsListView(PermissionMixin, ListView):
    model = FreqQuestions
    template_name = 'freqquestions/list.html'
    permission_required = 'view_freqquestions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('freqquestions_create')
        context['title'] = 'Listado de Preguntas frecuentes'
        return context


class FreqQuestionsCreateView(PermissionMixin, CreateView):
    model = FreqQuestions
    template_name = 'freqquestions/create.html'
    form_class = FreqQuestionsForm
    success_url = reverse_lazy('freqquestions_list')
    permission_required = 'add_freqquestions'

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
        context['title'] = 'Nuevo registro de una Pregunta frecuente'
        context['action'] = 'add'
        return context


class FreqQuestionsUpdateView(PermissionMixin, UpdateView):
    model = FreqQuestions
    template_name = 'freqquestions/create.html'
    form_class = FreqQuestionsForm
    success_url = reverse_lazy('freqquestions_list')
    permission_required = 'change_freqquestions'

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
        context['title'] = 'Edición de una Pregunta frecuente'
        context['action'] = 'edit'
        return context


class FreqQuestionsDeleteView(PermissionMixin, DeleteView):
    model = FreqQuestions
    template_name = 'freqquestions/delete.html'
    success_url = reverse_lazy('freqquestions_list')
    permission_required = 'delete_freqquestions'

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

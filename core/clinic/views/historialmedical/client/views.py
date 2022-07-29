import json

from django.http import HttpResponse
from django.views.generic import FormView

from core.clinic.forms import Sale, Mascots
from core.reports.forms import ReportForm
from core.security.mixins import ModuleMixin


class HistorialMedicalClientListView(ModuleMixin, FormView):
    form_class = ReportForm
    template_name = 'historialmedical/client/list.html'

    def get_form(self, form_class=None):
        form = ReportForm()
        form.fields['mascots'].queryset = Mascots.objects.filter(client__user=self.request.user)
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                mascot = request.POST['mascot']
                type = request.POST['type']
                search = Sale.objects.filter(mascot__client__user=request.user).exclude(type='venta').order_by('-date_joined')
                if len(mascot):
                    search = Sale.objects.filter(mascot_id=mascot)
                if len(type):
                    search = search.filter(type=type)
                for m in search:
                    data.append(m.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Historiales'
        return context

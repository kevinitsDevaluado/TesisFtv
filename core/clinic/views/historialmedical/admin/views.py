import json

from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import FormView

from core.clinic.forms import MedicalParameters, Sale, Mascots
from core.reports.forms import ReportForm
from core.security.mixins import ModuleMixin


class HistorialMedicalAdminListView(ModuleMixin, FormView):
    form_class = ReportForm
    template_name = 'historialmedical/admin/list.html'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                mascot = request.POST['mascot']
                type = request.POST['type']
                search = Sale.objects.filter().exclude(type='venta').order_by('date_joined')
                if len(mascot):
                    search = search.filter(mascot_id=mascot)
                if len(type):
                    search = search.filter(type=type)
                for m in search:
                    data.append(m.toJSON())
            elif action == 'search_mascot':
                data = []
                term = request.POST['term']
                for i in Mascots.objects.filter(
                        Q(client__user__first_name__icontains=term) |
                        Q(client__user__last_name__icontains=term) |
                        Q(name__icontains=term) |
                        Q(client__user__dni__icontains=term))[0:10]:
                    item = {'id': i.id, 'text': i.__str__()}
                    data.append(item)
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Historiales Vehiculo'
        context['medicalparameters'] = MedicalParameters.objects.all()
        return context

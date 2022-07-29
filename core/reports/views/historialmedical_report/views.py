import json

from django.http import HttpResponse
from django.views.generic import FormView

from core.clinic.models import Sale
from core.reports.forms import ReportForm
from core.security.mixins import ModuleMixin


class HistorialMedicalReportView(ModuleMixin, FormView):
    template_name = 'historialmedical_report/report.html'
    form_class = ReportForm

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'search_report':
                data = []
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                type = request.POST['type']
                search = Sale.objects.filter().exclude(type='venta').order_by('date_joined')
                if len(start_date) and len(end_date):
                    search = search.filter(date_joined__range=[start_date, end_date])
                if len(type):
                    search = search.filter(type=type)
                for m in search:
                    data.append(m.toJSON())
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Historial Vehicular'
        return context

import json

from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import FormView

from core.clinic.models import Client
from core.reports.forms import ReportForm
from core.security.mixins import ModuleMixin


class ClientReportView(ModuleMixin, FormView):
    template_name = 'client_report/report.html'
    form_class = ReportForm

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', None)
        data = {}
        try:
            if action == 'search_report':
                data = []
                term = self.request.POST['term']
                search = Client.objects.filter()
                if len(term):
                    search = search.filter(
                        Q(user__first_name__icontains=term) | Q(user__last_name__icontains=term) | Q(
                            user__dni__icontains=term))
                for i in search:
                    item = i.toJSON()
                    item['mascots'] = [m.toJSON() for m in i.mascots_set.all()]
                    data.append(item)
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Clientes'
        return context

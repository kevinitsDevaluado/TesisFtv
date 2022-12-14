import json

from django.http import HttpResponse
from django.views.generic import FormView

from core.clinic.models import Purchase
from core.reports.forms import ReportForm
from core.security.mixins import ModuleMixin


class PurchaseReportView(ModuleMixin, FormView):
    template_name = 'purchase_report/report.html'
    form_class = ReportForm

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'search_report':
                data = []
                start_date = self.request.POST['start_date']
                end_date = self.request.POST['end_date']
                search = Purchase.objects.filter()
                if len(start_date) and len(end_date):
                    search = search.filter(date_joined__range=[start_date, end_date])
                for i in search:
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Compras'
        return context

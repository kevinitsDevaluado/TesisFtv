import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DeleteView, FormView

from core.clinic.forms import *
from core.reports.forms import ReportForm
from core.security.mixins import PermissionMixin


class SaleAdminListView(PermissionMixin, FormView):
    form_class = ReportForm
    template_name = 'sale/admin/list.html'
    permission_required = 'view_sale_admin'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                search = Sale.objects.filter()
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                type_sale = request.POST['type_sale']
                pos = 1
                if len(start_date) and len(end_date):
                    search = search.filter(date_joined__range=[start_date, end_date])
                if len(type_sale):
                    search = search.filter(type=type_sale)
                for d in search.order_by('id'):
                    item = d.toJSON()
                    item['pos'] = pos
                    data.append(item)
                    pos += 1
            elif action == 'search_detproducts':
                data = []
                for det in SaleProducts.objects.filter(sale_id=request.POST['id']):
                    data.append(det.toJSON())
            elif action == 'search_detmedicalparameters':
                data = []
                for det in HistorialMedical.objects.filter(sale_id=request.POST['id']):
                    data.append(det.toJSON())
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Ventas'
        return context


class SaleAdminDeleteView(PermissionMixin, DeleteView):
    model = Sale
    template_name = 'sale/admin/delete.html'
    success_url = reverse_lazy('sale_admin_list')
    permission_required = 'delete_sale_admin'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            sale = self.get_object()
            sale.delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context

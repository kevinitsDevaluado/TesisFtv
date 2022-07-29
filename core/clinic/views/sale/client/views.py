import json
from datetime import datetime

from django.db import transaction
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView

from core.clinic.forms import Sale, SaleProducts, HistorialMedical, SaleForm, Mascots, Employee
from core.reports.forms import ReportForm
from core.security.mixins import PermissionMixin


class SaleClientListView(PermissionMixin, FormView):
    form_class = ReportForm
    template_name = 'sale/client/list.html'
    permission_required = 'view_sale_client'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                search = Sale.objects.filter(mascot__client__user=request.user)
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
        # context['create_url'] = reverse_lazy('sale_client_create')
        context['title'] = 'Listado de Citas Agendadas'
        return context


class SaleClienCreateView(PermissionMixin, CreateView):
    model = Sale
    template_name = 'sale/client/create.html'
    form_class = SaleForm
    success_url = reverse_lazy('sale_client_list')
    permission_required = 'add_sale_client'

    def get_form(self, form_class=None):
        form = SaleForm()
        form.fields['mascot'].queryset = Mascots.objects.filter(client=self.request.user.client)
        return form

    def search_quotes(self):
        data = []
        try:
            date_current = datetime.now()
            employee = self.request.POST['employee']
            date_joined = self.request.POST['date_joined']
            if len(employee) and len(date_joined):
                date_joined = datetime.strptime(date_joined, '%Y-%m-%d')
                pos = 0
                for h in range(8, 19):
                    hour = h
                    if h < 10:
                        hour = '0{}'.format(h)
                    for minute in ['00']:
                        clock = datetime(year=date_joined.year, month=date_joined.month, day=date_joined.day,
                                         hour=int(hour), minute=int(minute))
                        status = 'vacant'
                        hist = Sale.objects.filter(date_joined=date_joined,
                                                   employee_id=employee,
                                                   hour=clock.time(),
                                                   type='cita_medica',
                                                   status='activo')
                        if hist.exists():
                            status = 'reserved'
                        elif date_current > clock:
                            status = 'time_not_available'
                        data.append({
                            'pos': pos,
                            'hour': clock.time().strftime('%H:%M'),
                            'status': status
                        })
                        if h == 18:
                            break
                        pos += 1
        except:
            pass
        return data

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'add':
                with transaction.atomic():
                    vent = Sale()
                    vent.type = 'cita_medica'
                    vent.mascot_id = int(request.POST['mascot'])
                    vent.employee_id = int(request.POST['employee'])
                    vent.date_joined = datetime.strptime(request.POST['date_joined'], '%Y-%m-%d')
                    vent.hour = datetime.strptime(request.POST['hour'], '%H:%M').time()
                    vent.symptoms = request.POST['symptoms']
                    vent.status = 'activo'
                    vent.save()

                    msg = 'Cita agendada correctamente para el dia {} a las {}'.format(
                        vent.date_joined.strftime('%Y-%m-%d'),
                        vent.hour.strftime('%H:%M %p')
                    )

                    data = {'msg': msg}
            elif action == 'search_quotes':
                data = self.search_quotes()
            elif action == 'search_employee':
                data = Employee.objects.get(id=request.POST['id']).toJSON()
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de una Cita'
        context['action'] = 'add'
        return context
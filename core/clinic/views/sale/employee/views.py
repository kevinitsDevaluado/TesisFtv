import json

from django.contrib.auth.models import Group
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, FormView, UpdateView

from core.clinic.forms import *
from core.homepage.models import Mainpage
from core.reports.forms import ReportForm
from core.security.mixins import PermissionMixin


class SaleEmployeeListView(PermissionMixin, FormView):
    form_class = ReportForm
    template_name = 'sale/employee/list.html'
    permission_required = 'view_sale_employee'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                search = Sale.objects.filter(employee__user=request.user)
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
        context['create_url'] = reverse_lazy('sale_employee_create')
        context['title'] = 'Listado de Citas del Dia'
        return context


class SaleEmployeeCreateView(PermissionMixin, CreateView):
    model = Sale
    template_name = 'sale/employee/create.html'
    form_class = SaleForm
    success_url = reverse_lazy('sale_employee_list')
    permission_required = 'add_sale_employee'

    def validate_client(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            id = self.request.POST['id'].strip()
            clients = Client.objects.filter()
            users = User.objects.filter()
            if len(id):
                clients = clients.exclude(id=id)
                users = users.exclude(client_id=id)
            if type == 'dni':
                if users.filter(dni=obj):
                    data['valid'] = False
            elif type == 'email':
                if users.filter(email=obj):
                    data['valid'] = False
            elif type == 'mobile':
                if clients.filter(mobile=obj):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'add':
                with transaction.atomic():
                    vent = Sale()
                    print(request.POST)
                    vent.type = request.POST['type']
                    vent.mascot_id = int(request.POST['mascot'])
                    vent.employee_id = request.user.employee.id
                    vent.date_joined = request.POST['date_joined']
                    vent.observation = request.POST['observation']
                    vent.iva = float(request.POST['iva']) / 100
                    vent.status = 'finalizado'
                    if vent.type == 'cita_medica':
                        vent.symptoms = request.POST['symptoms']
                        vent.diagnosis = request.POST['diagnosis']
                    vent.save()

                    for i in json.loads(request.POST['products']):
                        det = SaleProducts()
                        det.sale_id = vent.id
                        det.product_id = int(i['id'])
                        det.cant = int(i['cant'])
                        det.price = float(i['price'])
                        det.subtotal = det.cant * det.price
                        det.save()

                        if det.product.producttype.has_stock:
                            det.product.stock -= det.cant
                            det.product.save()

                    if vent.type in ['control_vacuna', 'control_antiparasitario', 'cita_medica']:
                        for p in json.loads(request.POST['medical_parameters']):
                            det = HistorialMedical()
                            det.sale_id = vent.id
                            det.medical_parameters_id = int(p['id'])
                            det.valor = p['valor']
                            det.desc = p['desc']
                            det.save()

                    vent.calculate_invoice()

                    data = {'id': vent.id}
            elif action == 'search_products':
                ids = json.loads(request.POST['ids'])
                data = []
                term = request.POST['term']
                search = Product.objects.filter().exclude(id__in=ids).order_by(
                    'name')
                if len(term):
                    search = search.filter(name__icontains=term)
                    search = search[:10]
                for p in search:
                    if p.stock > 0 or not p.producttype.has_stock:
                        item = p.toJSON()
                        item['value'] = '{} / {}'.format(p.name, p.producttype.name)
                        data.append(item)
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
            elif action == 'search_medicalparameters':
                data = []
                mascot = request.POST['mascot']
                for i in MedicalParameters.objects.filter():
                    item = i.toJSON()
                    item['valor'] = '0.00'
                    item['last_valor'] = i.get_last(mascot)
                    item['desc'] = ''
                    data.append(item)
            elif action == 'validate_client':
                return self.validate_client()
            elif action == 'search_client':
                data = []
                term = request.POST['term']
                for i in Client.objects.filter(user__dni__icontains=term)[
                         0:10]:
                    item = i.toJSON()
                    item['value'] = i.user.dni
                    data.append(item)
            elif action == 'create_mascot':
                with transaction.atomic():
                    id_client = request.POST['id_client']
                    client = Client()
                    if len(id_client) == 0:
                        user = User()
                        user.first_name = request.POST['first_name']
                        user.last_name = request.POST['last_name']
                        user.dni = request.POST['dni']
                        user.create_or_update_password(user.dni)
                        user.email = request.POST['email']
                        user.save()
                        client.user_id = user.id
                        client.mobile = request.POST['mobile']
                        client.address = request.POST['address']
                        client.save()
                        group = Group.objects.get(pk=settings.GROUPS.get('client'))
                        user.groups.add(group)
                    else:
                        client = Client.objects.get(pk=id_client)
                    mascot = Mascots()
                    mascot.client_id = client.id
                    mascot.name = request.POST['name']
                    mascot.color_id = int(request.POST['color'])
                    mascot.breed_id = int(request.POST['breed'])
                    mascot.gender = request.POST['gender']
                    mascot.save()

                    instance = Mascots.objects.get(pk=mascot.id)
                    data = instance.toJSON()
                    data['text'] = instance.__str__()
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de una Venta'
        context['action'] = 'add'
        context['iva'] = format(Mainpage.objects.first().iva, '.2f')
        context['clientForm'] = ClientForm()
        context['mascotsForm'] = MascotsForm()
        return context


class SaleEmployeeAttendView(PermissionMixin, UpdateView):
    model = Sale
    template_name = 'sale/employee/create.html'
    form_class = SaleForm
    success_url = reverse_lazy('sale_employee_list')
    permission_required = 'attend_mascots_employee'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def validate_client(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            id = self.request.POST['id'].strip()
            clients = Client.objects.filter()
            users = User.objects.filter()
            if len(id):
                clients = clients.exclude(id=id)
                users = users.exclude(client_id=id)
            if type == 'dni':
                if users.filter(dni=obj):
                    data['valid'] = False
            elif type == 'email':
                if users.filter(email=obj):
                    data['valid'] = False
            elif type == 'mobile':
                if clients.filter(mobile=obj):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def get_form(self, form_class=None):
        instance = self.get_object()
        form = SaleForm(instance=instance, initial={
            'symptoms': instance.symptoms
        })
        form.fields['mascot'].queryset = Mascots.objects.filter(pk=instance.mascot.id)
        return form

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'attend':
                with transaction.atomic():
                    vent = self.object
                    vent.type = request.POST['type']
                    vent.mascot_id = int(request.POST['mascot'])
                    vent.employee_id = request.user.employee.id
                    vent.date_joined = request.POST['date_joined']
                    vent.observation = request.POST['observation']
                    vent.iva = float(request.POST['iva']) / 100
                    vent.status = 'finalizado'
                    if vent.type == 'cita_medica':
                        vent.symptoms = request.POST['symptoms']
                        vent.diagnosis = request.POST['diagnosis']
                    vent.save()

                    for i in json.loads(request.POST['products']):
                        det = SaleProducts()
                        det.sale_id = vent.id
                        det.product_id = int(i['id'])
                        det.cant = int(i['cant'])
                        det.price = float(i['price'])
                        det.subtotal = det.cant * det.price
                        det.save()

                        if det.product.producttype.has_stock:
                            det.product.stock -= det.cant
                            det.product.save()

                    if vent.type in ['control_vacuna', 'control_antiparasitario', 'cita_medica']:
                        for p in json.loads(request.POST['medical_parameters']):
                            det = HistorialMedical()
                            det.sale_id = vent.id
                            det.medical_parameters_id = int(p['id'])
                            det.valor = p['valor']
                            det.desc = p['desc']
                            det.save()

                    vent.calculate_invoice()

                    data = {'id': vent.id}
            elif action == 'search_products':
                ids = json.loads(request.POST['ids'])
                data = []
                term = request.POST['term']
                search = Product.objects.filter().exclude(id__in=ids).order_by(
                    'name')
                if len(term):
                    search = search.filter(name__icontains=term)
                    search = search[:10]
                for p in search:
                    if p.stock > 0 or not p.producttype.has_stock:
                        item = p.toJSON()
                        item['value'] = '{} / {}'.format(p.name, p.producttype.name)
                        data.append(item)
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
            elif action == 'search_medicalparameters':
                data = []
                mascot = request.POST['mascot']
                for i in MedicalParameters.objects.filter():
                    item = i.toJSON()
                    item['valor'] = '0.00'
                    item['last_valor'] = i.get_last(mascot)
                    item['desc'] = ''
                    data.append(item)
            elif action == 'validate_client':
                return self.validate_client()
            elif action == 'search_client':
                data = []
                term = request.POST['term']
                for i in Client.objects.filter(user__dni__icontains=term)[
                         0:10]:
                    item = i.toJSON()
                    item['value'] = i.user.dni
                    data.append(item)
            elif action == 'create_mascot':
                with transaction.atomic():
                    id_client = request.POST['id_client']
                    client = Client()
                    if len(id_client) == 0:
                        user = User()
                        user.first_name = request.POST['first_name']
                        user.last_name = request.POST['last_name']
                        user.dni = request.POST['dni']
                        user.create_or_update_password(user.dni)
                        user.email = request.POST['email']
                        user.save()
                        client.user_id = user.id
                        client.mobile = request.POST['mobile']
                        client.address = request.POST['address']
                        client.save()
                        group = Group.objects.get(pk=settings.GROUPS.get('client'))
                        user.groups.add(group)
                    else:
                        client = Client.objects.get(pk=id_client)
                    mascot = Mascots()
                    mascot.client_id = client.id
                    mascot.name = request.POST['name']
                    mascot.color_id = int(request.POST['color'])
                    mascot.breed_id = int(request.POST['breed'])
                    mascot.gender = request.POST['gender']
                    mascot.save()

                    instance = Mascots.objects.get(pk=mascot.id)
                    data = instance.toJSON()
                    data['text'] = instance.__str__()
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Atención'
        context['action'] = 'attend'
        context['iva'] = format(Mainpage.objects.first().iva, '.2f')
        context['clientForm'] = ClientForm()
        context['mascotsForm'] = MascotsForm()
        return context


class SaleEmployeeDeleteView(PermissionMixin, DeleteView):
    model = Sale
    template_name = 'sale/employee/delete.html'
    success_url = reverse_lazy('sale_employee_list')
    permission_required = 'delete_sale_employee'

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

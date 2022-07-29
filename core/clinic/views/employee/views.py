import json

from django.contrib.auth.models import Group
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView

from config import settings
from core.clinic.forms import EmployeeForm, User, Employee, Parish
from core.security.mixins import ModuleMixin, PermissionMixin


class EmployeeListView(PermissionMixin, TemplateView):
    template_name = 'employee/list.html'
    permission_required = 'view_employee'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                for i in Employee.objects.filter():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('employee_create')
        context['title'] = 'Listado de Empleados'
        return context


class EmployeeCreateView(PermissionMixin, CreateView):
    model = Employee
    template_name = 'employee/create.html'
    form_class = EmployeeForm
    success_url = reverse_lazy('employee_list')
    permission_required = 'add_employee'

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            if type == 'dni':
                if User.objects.filter(dni=obj):
                    data['valid'] = False
            elif type == 'mobile':
                if Employee.objects.filter(mobile=obj):
                    data['valid'] = False
            elif type == 'email':
                if User.objects.filter(email=obj):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                with transaction.atomic():
                    user = User()
                    user.first_name = request.POST['first_name']
                    user.last_name = request.POST['last_name']
                    user.dni = request.POST['dni']
                    user.username = user.dni
                    if 'image' in request.FILES:
                        user.image = request.FILES['image']
                    user.create_or_update_password(user.dni)
                    user.email = request.POST['email']
                    user.save()

                    employee = Employee()
                    employee.user_id = user.id
                    employee.gender = request.POST['gender']
                    employee.mobile = request.POST['mobile']
                    employee.phone = request.POST['phone']
                    employee.address = request.POST['address']
                    employee.birthdate = request.POST['birthdate']
                    employee.parish_id = int(request.POST['parish'])
                    employee.profession_id = int(request.POST['profession'])
                    if 'curriculum' in request.FILES:
                        employee.curriculum = request.FILES['curriculum']
                    employee.save()
                    group = Group.objects.get(pk=settings.GROUPS.get('employee'))
                    user.groups.add(group)
            elif action == 'search_parish':
                data = []
                term = request.POST['term']
                for i in Parish.objects.filter(name__icontains=term)[0:10]:
                    item = {'id': i.id, 'text': i.__str__(), 'data': i.toJSON()}
                    data.append(item)
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de un Empleado'
        context['action'] = 'add'
        context['instance'] = None
        return context


class EmployeeUpdateView(PermissionMixin, UpdateView):
    model = Employee
    template_name = 'employee/create.html'
    form_class = EmployeeForm
    success_url = reverse_lazy('employee_list')
    permission_required = 'change_employee'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        instance = self.object
        form = EmployeeForm(instance=instance, initial={
            'first_name': instance.user.first_name,
            'last_name': instance.user.last_name,
            'dni': instance.user.dni,
            'email': instance.user.email,
            'image': instance.user.image,
        })
        if instance.parish:
            form.fields['parish'].queryset = Parish.objects.filter(id=instance.parish.id)
        return form

    def validate_data(self):
        data = {'valid': True}
        try:
            instance = self.object
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            if type == 'dni':
                if User.objects.filter(dni=obj).exclude(id=instance.user.id):
                    data['valid'] = False
            elif type == 'mobile':
                if Employee.objects.filter(mobile=obj).exclude(id=instance.id):
                    data['valid'] = False
            elif type == 'email':
                if User.objects.filter(email=obj).exclude(id=instance.user.id):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                with transaction.atomic():
                    instance = self.object
                    user = instance.user
                    user.first_name = request.POST['first_name']
                    user.last_name = request.POST['last_name']
                    user.dni = request.POST['dni']
                    user.username = user.dni
                    if 'image-clear' in request.POST:
                        user.remove_image()
                        user.image = None
                    if 'image' in request.FILES:
                        user.image = request.FILES['image']
                    user.email = request.POST['email']
                    user.save()

                    employee = instance
                    employee.user_id = user.id
                    employee.gender = request.POST['gender']
                    employee.mobile = request.POST['mobile']
                    employee.phone = request.POST['phone']
                    employee.address = request.POST['address']
                    employee.birthdate = request.POST['birthdate']
                    employee.parish_id = int(request.POST['parish'])
                    employee.profession_id = int(request.POST['profession'])
                    if 'curriculum-clear' in request.POST:
                        employee.remove_curriculum()
                        employee.curriculum = None
                    if 'curriculum' in request.FILES:
                        employee.curriculum = request.FILES['curriculum']
                    employee.save()
            elif action == 'search_parish':
                data = []
                term = request.POST['term']
                for i in Parish.objects.filter(name__icontains=term)[0:10]:
                    item = {'id': i.id, 'text': i.__str__(), 'data': i.toJSON()}
                    data.append(item)
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de un Empleado'
        context['action'] = 'edit'
        context['instance'] = self.object
        return context


class EmployeeDeleteView(PermissionMixin, DeleteView):
    model = Employee
    template_name = 'employee/delete.html'
    success_url = reverse_lazy('employee_list')
    permission_required = 'delete_employee'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            with transaction.atomic():
                instance = self.get_object()
                user = instance.user
                instance.delete()
                user.delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context


class EmployeeUpdateProfileView(ModuleMixin, UpdateView):
    model = Employee
    template_name = 'employee/profile.html'
    form_class = EmployeeForm
    success_url = reverse_lazy('dashboard')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user.employee

    def get_form(self, form_class=None):
        instance = self.object
        form = EmployeeForm(instance=instance, initial={
            'first_name': instance.user.first_name,
            'last_name': instance.user.last_name,
            'dni': instance.user.dni,
            'email': instance.user.email,
            'image': instance.user.image,
        })
        if instance.parish:
            form.fields['parish'].queryset = Parish.objects.filter(id=instance.parish.id)
        return form

    def validate_data(self):
        data = {'valid': True}
        try:
            instance = self.object
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            if type == 'dni':
                if User.objects.filter(dni=obj).exclude(id=instance.user.id):
                    data['valid'] = False
            elif type == 'mobile':
                if Employee.objects.filter(mobile=obj).exclude(id=instance.id):
                    data['valid'] = False
            elif type == 'email':
                if User.objects.filter(email=obj).exclude(id=instance.user.id):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                with transaction.atomic():
                    instance = self.object
                    user = instance.user
                    user.first_name = request.POST['first_name']
                    user.last_name = request.POST['last_name']
                    user.dni = request.POST['dni']
                    user.username = user.dni
                    if 'image-clear' in request.POST:
                        user.remove_image()
                        user.image = None
                    if 'image' in request.FILES:
                        user.image = request.FILES['image']
                    user.email = request.POST['email']
                    user.save()

                    employee = instance
                    employee.user_id = user.id
                    employee.gender = request.POST['gender']
                    employee.mobile = request.POST['mobile']
                    employee.phone = request.POST['phone']
                    employee.address = request.POST['address']
                    employee.birthdate = request.POST['birthdate']
                    employee.parish_id = int(request.POST['parish'])
                    employee.profession_id = int(request.POST['profession'])
                    if 'curriculum-clear' in request.POST:
                        employee.remove_curriculum()
                        employee.curriculum = None
                    if 'curriculum' in request.FILES:
                        employee.curriculum = request.FILES['curriculum']
                    employee.save()
            elif action == 'search_parish':
                data = []
                term = request.POST['term']
                for i in Parish.objects.filter(name__icontains=term)[0:10]:
                    item = {'id': i.id, 'text': i.__str__(), 'data': i.toJSON()}
                    data.append(item)
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de Perfil'
        context['action'] = 'edit'
        context['instance'] = self.object
        return context

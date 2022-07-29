import os
from datetime import datetime

from django.db import models
from django.forms import model_to_dict

from config import settings
from core.clinic.choices import *   
from core.homepage.models import Mainpage
from core.user.models import User


class Country(models.Model):
    code = models.CharField(max_length=10, verbose_name='Código', unique=True)
    name = models.CharField(max_length=50, verbose_name='Nombre', unique=True)

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'País'
        verbose_name_plural = 'Paises'
        ordering = ['-id']


class Province(models.Model):
    country = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name='País')
    name = models.CharField(max_length=50, verbose_name='Nombre', unique=True)
    code = models.CharField(max_length=10, verbose_name='Código', unique=True)

    def __str__(self):
        return 'País: {} / Provincia: {}'.format(self.country.name, self.name)

    def toJSON(self):
        item = model_to_dict(self)
        item['country'] = self.country.toJSON()
        return item

    class Meta:
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'
        ordering = ['-id']


class Canton(models.Model):
    province = models.ForeignKey(Province, on_delete=models.PROTECT, verbose_name='Provincia')
    name = models.CharField(max_length=50, verbose_name='Nombre')

    def __str__(self):
        return '{} / Cantón: {}'.format(self.province.__str__(), self.name)

    def toJSON(self):
        item = model_to_dict(self)
        item['province'] = self.province.toJSON()
        return item

    class Meta:
        verbose_name = 'Cantón'
        verbose_name_plural = 'Cantones'
        ordering = ['-id']


class Parish(models.Model):
    canton = models.ForeignKey(Canton, on_delete=models.PROTECT, verbose_name='Cantón')
    name = models.CharField(max_length=100, verbose_name='Nombre')

    def __str__(self):
        return '{} / Parroquia: {}'.format(self.canton.__str__(), self.name)

    def toJSON(self):
        item = model_to_dict(self)
        item['canton'] = self.canton.toJSON()
        return item

    class Meta:
        verbose_name = 'Parroquia'
        verbose_name_plural = 'Parroquias'
        ordering = ['-id']


class Profession(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre', unique=True)

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Profesión'
        verbose_name_plural = 'Profesiones'
        ordering = ['-id']


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    gender = models.CharField(max_length=10, choices=gender_person, default=gender_person[0][0], verbose_name='Sexo')
    mobile = models.CharField(max_length=10, unique=True, verbose_name='Teléfono celular')
    phone = models.CharField(max_length=10, null=True, blank=True, verbose_name='Teléfono convencional')
    address = models.CharField(max_length=500, null=True, blank=True, verbose_name='Dirección')
    birthdate = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')
    parish = models.ForeignKey(Parish, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Parroquia')

    def __str__(self):
        return '{} / {}'.format(self.user.get_full_name(), self.user.dni)

    def toJSON(self):
        item = model_to_dict(self)
        item['user'] = self.user.toJSON()
        item['birthdate'] = self.birthdate.strftime('%Y-%m-%d')
        item['gender'] = {'id': self.gender, 'name': self.get_gender_display()}
        item['parish'] = {} if self.parish is None else self.parish.toJSON()
        return item

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['-id']


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    gender = models.CharField(max_length=10, choices=gender_person, default=gender_person[0][0], verbose_name='Sexo')
    mobile = models.CharField(max_length=10, unique=True, verbose_name='Teléfono celular')
    phone = models.CharField(max_length=10, null=True, blank=True, verbose_name='Teléfono convencional')
    address = models.CharField(max_length=500, null=True, blank=True, verbose_name='Dirección')
    birthdate = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')
    parish = models.ForeignKey(Parish, on_delete=models.PROTECT, verbose_name='Profesión')
    profession = models.ForeignKey(Profession, null=True, blank=True, on_delete=models.PROTECT)
    curriculum = models.FileField(upload_to='curriculum/%Y/%m/%d', null=True, blank=True)

    def __str__(self):
        return '{} / {} / {}'.format(self.user.get_full_name(), self.user.dni, self.profession.name)

    def get_curriculum(self):
        if self.curriculum:
            return '{}{}'.format(settings.MEDIA_URL, self.curriculum)
        return ''

    def remove_curriculum(self):
        try:
            if self.curriculum:
                os.remove(self.curriculum.path)
        except:
            pass

    def toJSON(self):
        item = model_to_dict(self, exclude=[])
        item['user'] = self.user.toJSON()
        item['gender'] = {'id': self.gender, 'name': self.get_gender_display()}
        item['parish'] = {} if self.parish is None else self.parish.toJSON()
        item['profession'] = {} if self.profession is None else self.profession.toJSON()
        item['birthdate'] = self.birthdate.strftime('%Y-%m-%d')
        item['curriculum'] = self.get_curriculum()
        return item

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        ordering = ['-id']


class Provider(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Nombre')
    ruc = models.CharField(max_length=13, unique=True, verbose_name='Ruc')
    mobile = models.CharField(max_length=10, unique=True, verbose_name='Teléfono celular')
    address = models.CharField(max_length=500, null=True, blank=True, verbose_name='Dirección')
    email = models.CharField(max_length=50, unique=True, verbose_name='Email')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['-id']


class ProductType(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Nombre')
    has_stock = models.BooleanField(default=True, verbose_name='Tiene stock')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Tipo de Producto'
        verbose_name_plural = 'Tipos de Productos'
        ordering = ['-id']


class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre')
    desc = models.CharField(max_length=50, verbose_name='Descripción', null=True, blank=True)
    producttype = models.ForeignKey(ProductType, on_delete=models.PROTECT, verbose_name='Tipo de Producto')
    image = models.ImageField(upload_to='products/%Y/%m/%d', verbose_name='Imagen', null=True, blank=True)
    price = models.DecimalField(default=0.00, decimal_places=2, max_digits=9, verbose_name='Precio Venta')
    pvc = models.DecimalField(default=0.00, decimal_places=2, max_digits=9, verbose_name='Precio Compra')
    stock = models.IntegerField(default=0)

    def __str__(self):
        return 'Nombre: {} / Precio: ${}'.format(self.name, format(self.price, '.2f'))

    def get_desc(self):
        if self.desc:
            return self.desc
        return 'Sin descripción'

    def get_image(self):
        if self.image:
            return '{}{}'.format(settings.MEDIA_URL, self.image)
        return '{}{}'.format(settings.STATIC_URL, 'img/default/empty.png')

    def toJSON(self):
        item = model_to_dict(self)
        item['price'] = format(self.price, '.2f')
        item['pvc'] = format(self.price, '.2f')
        item['producttype'] = self.producttype.toJSON()
        item['image'] = self.get_image()
        return item

    def delete(self, using=None, keep_parents=False):
        try:
            os.remove(self.image.path)
        except:
            pass
        super(Product, self).delete()

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-id']


class Purchase(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.PROTECT)
    date_joined = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return self.provider.name

    def calculate_invoice(self):
        subtotal = 0.00
        for d in self.purchasedetail_set.all():
            subtotal += float(d.price) * int(d.cant)
        self.subtotal = subtotal
        self.save()

    def delete(self, using=None, keep_parents=False):
        try:
            for d in self.purchasedetail_set.filter(product__producttype__has_stock=True):
                d.product.stock -= d.cant
                d.product.save()
        except:
            pass
        super(Purchase, self).delete()

    def toJSON(self):
        item = model_to_dict(self)
        item['nro'] = format(self.id, '06d')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['provider'] = self.provider.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
        default_permissions = ()
        permissions = (
            ('view_purchase', 'Can view Compras'),
            ('add_purchase', 'Can add Compras'),
            ('delete_purchase', 'Can delete Compras'),
        )
        ordering = ['-id']


class PurchaseDetail(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    cant = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return self.product.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['purchase'])
        item['product'] = self.product.toJSON()
        item['price'] = format(self.price, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Det.Compra'
        verbose_name_plural = 'Det.Compras'
        default_permissions = ()
        ordering = ['-id']


class Color(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre', unique=True)
    hex = models.CharField(max_length=50, verbose_name='Código', unique=True)

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Color'
        verbose_name_plural = 'Colores'
        ordering = ['-id']


class TypePet(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre', unique=True)

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Tipo de Mascota'
        verbose_name_plural = 'Tipo de Mascotas'
        ordering = ['-id']


class BreedPet(models.Model):
    type = models.ForeignKey(TypePet, on_delete=models.PROTECT, verbose_name='Tipo de Mascota')
    name = models.CharField(max_length=50, verbose_name='Nombre')

    def __str__(self):
        return self.name

    def format_name(self):
        return 'Tipo de Animal: {} / Tipo de Raza: {}'.format(self.type.name, self.name)

    def toJSON(self):
        item = model_to_dict(self)
        item['type'] = self.type.toJSON()
        return item

    class Meta:
        verbose_name = 'Raza de Mascota'
        verbose_name_plural = 'Razas de Mascotas'
        ordering = ['-id']


class Mascots(models.Model):
    date_joined = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=150, verbose_name='Placa')
    client = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name='Cliente')
    color = models.ForeignKey(Color, on_delete=models.PROTECT, verbose_name='Color',default='')
    image = models.ImageField(upload_to='mascots/%Y/%m/%d', verbose_name='Imagen', null=True, blank=True)
    breed = models.ForeignKey(BreedPet, on_delete=models.PROTECT, verbose_name='Tipo de Raza',default='')
    gender = models.CharField(max_length=10, choices=gender_pet, default=gender_pet[0][0], verbose_name='Sexo')
    birthdate = models.DateField(default=datetime.now, verbose_name='Fecha de cumpleaños'   )
    observation = models.CharField(max_length=5000, null=True, blank=True, verbose_name='Observación')

    def __str__(self):
        return 'Nombre: {} / Dueño: {} '.format(self.name,
                                                                                 self.client.user.get_full_name(),
                                                                                 )

    def short_name(self):
        return 'Nombre: {} / Raza: {} / Tipo: {} / Color: {}'.format(self.name,
                                                                     self.breed.name,
                                                                     self.breed.type.name,
                                                                     self.color.name)

    def get_image(self):
        if self.image:
            return '{}{}'.format(settings.MEDIA_URL, self.image)
        return '{}{}'.format(settings.STATIC_URL, 'img/default/empty.png')

    def get_age(self):
        age = datetime.now().year - self.birthdate.year
        return age

    def remove_image(self):
        try:
            if self.image:
                os.remove(self.image.path)
        except:
            pass

    def toJSON(self):
        item = model_to_dict(self, exclude=['user'])
        item['gender'] = {'id': self.gender, 'name': self.get_gender_display()}
        item['breed'] = self.breed.toJSON()
        item['color'] = self.color.toJSON()
        item['client'] = self.client.toJSON()
        item['image'] = self.get_image()
        item['birthdate'] = self.birthdate.strftime('%Y-%m-%d')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['age'] = self.get_age()
        return item

    def delete(self, using=None, keep_parents=False):
        try:
            os.remove(self.image.path)
        except:
            pass
        super(Mascots, self).delete()

    class Meta:
        verbose_name = 'Mascota'
        verbose_name_plural = 'Mascotas'
        default_permissions = ()
        permissions = (
            ('view_mascots_admin', 'Can view Mascotas | Admin'),
            ('add_mascots_admin', 'Can add Mascotas | Admin'),
            ('change_mascots_admin', 'Can change Mascotas | Admin'),
            ('delete_mascots_admin', 'Can delete Mascotas | Admin'),
            ('view_mascots_client', 'Can view Mascotas | Client'),
            ('add_mascots_client', 'Can add Mascotas | Client'),
            ('change_mascots_client', 'Can change Mascotas | Client'),
            ('delete_mascots_client', 'Can delete Mascotas | Client'),
        )
        ordering = ['-id']


class MedicalParameters(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre', unique=True)

    def __str__(self):
        return self.name

    def get_last(self, mascot_id):
        if len(mascot_id):
            hismed = self.historialmedical_set.filter(sale__mascot_id=mascot_id).order_by('-id')
            if hismed.exists():
                return hismed[0].valor
        return ''

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Parámetro Médico'
        verbose_name_plural = 'Parámetros Médicos'
        ordering = ['-id']


class Sale(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    mascot = models.ForeignKey(Mascots, on_delete=models.PROTECT)
    type = models.CharField(max_length=50, choices=type_sale, default='venta')
    date_joined = models.DateField(default=datetime.now)
    hour = models.TimeField(default=datetime.now)
    observation = models.CharField(max_length=5000, null=True, blank=True)
    symptoms = models.CharField(max_length=5000, null=True, blank=True)
    diagnosis = models.CharField(max_length=5000, null=True, blank=True)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total_iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    status = models.CharField(max_length=30, choices=type_status, default='finalizado')

    def __str__(self):
        return self.mascot.name

    def nro(self):
        return format(self.id, '06d')

    def calculate_invoice(self):
        subtotal = 0.00
        for d in self.saleproducts_set.all():
            subtotal += float(d.price) * int(d.cant)
        self.subtotal = subtotal
        self.total_iva = float(self.iva) * float(self.subtotal)
        self.total = float(self.subtotal) + float(self.total_iva)
        self.save()

    def get_nro(self):
        return format(self.id, '06d')

    def get_observation(self):
        if self.observation:
            return self.observation
        return 'Ninguna'

    def delete(self, using=None, keep_parents=False):
        try:
            for det in self.saleproducts_set.filter(product__producttype__has_stock=True):
                det.product.stock += det.cant
                det.product.save()
                det.delete()
        except:
            pass
        super(Sale, self).delete()

    def toJSON(self):
        item = model_to_dict(self)
        item['type'] = {'id': self.type, 'name': self.get_type_display()}
        item['status'] = {'id': self.status, 'name': self.get_status_display()}
        item['employee'] = self.employee.toJSON()
        item['hour'] = self.hour.strftime('%H:%M %p')
        item['mascot'] = self.mascot.toJSON()
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['total'] = format(self.total, '.2f')
        item['total_iva'] = format(self.total_iva, '.2f')
        item['observation'] = self.get_observation()
        item['historialmedical'] = [h.toJSON() for h in self.historialmedical_set.all()]
        return item

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        default_permissions = ()
        permissions = (
            ('view_sale_admin', 'Can view Ventas |Admin'),
            ('delete_sale_admin', 'Can delete Ventas | Admin'),
            ('view_sale_client', 'Can view Ventas | Client'),
            ('add_sale_client', 'Can add Ventas | Client'),
            ('view_sale_employee', 'Can view Ventas | Employee'),
            ('add_sale_employee', 'Can add Ventas | Employee'),
            ('delete_sale_employee', 'Can delete Ventas | Employee'),
            ('attend_mascots_employee', 'Can attend Ventas| Employee'),
        )
        ordering = ['-id']


class HistorialMedical(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    medical_parameters = models.ForeignKey(MedicalParameters, on_delete=models.PROTECT)
    valor = models.CharField(max_length=100)
    desc = models.CharField(max_length=5000, null=True, blank=True)

    def __str__(self):
        return self.sale.mascot.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['medical_parameters'] = self.medical_parameters.toJSON()
        return item

    class Meta:
        verbose_name = 'Historial Médico'
        verbose_name_plural = 'Historiales Médicos'
        default_permissions = ()
        ordering = ['-id']


class SaleProducts(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    cant = models.IntegerField(default=0)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.product.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['product'] = self.product.toJSON()
        item['price'] = format(self.price, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Venta de Producto'
        verbose_name_plural = 'Venta de Productos'
        default_permissions = ()
        ordering = ['-id']

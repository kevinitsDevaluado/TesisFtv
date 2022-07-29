import os

from django.db import models
from django.forms import model_to_dict

from datetime import datetime

from config import settings


class Mainpage(models.Model):
    name = models.CharField(verbose_name='Nombre', max_length=50)
    ruc = models.CharField(verbose_name='Ruc', max_length=13)
    proprietor = models.CharField(verbose_name='Propietario', max_length=100)
    desc = models.CharField(verbose_name='Descripción', max_length=2000, blank=True, null=True)
    with_us = models.CharField(verbose_name='¿Porque estar con nosotros?', max_length=2000, blank=True, null=True)
    mission = models.CharField(verbose_name='Misión', max_length=1000, blank=True, null=True)
    vision = models.CharField(verbose_name='Visión', max_length=1000, blank=True, null=True)
    about_us = models.CharField(verbose_name='Quienes Somos', max_length=1000, blank=True, null=True)
    icon_image = models.ImageField(verbose_name='Logo', upload_to='mainpage/%Y/%m/%d', null=True, blank=True)
    phone = models.CharField(verbose_name='Teléfono Convencional', max_length=9, unique=True, blank=True, null=True)
    mobile = models.CharField(verbose_name='Teléfono Celular', max_length=10, unique=True, blank=True, null=True)
    email = models.EmailField(verbose_name='Correo Electrónico', max_length=50, unique=True, blank=True, null=True)
    address = models.CharField(verbose_name='Dirección', max_length=255, blank=True, null=True)
    horary = models.CharField(verbose_name='Horario', max_length=50, blank=True, null=True)
    experiencia = models.CharField(verbose_name='Experiencia', max_length=50, blank=True, null=True,default='')
    coordinates = models.CharField(verbose_name='Coordenadas', max_length=50, blank=True, null=True)
    about_youtube = models.CharField(verbose_name='Video de Youtube', max_length=250, blank=True, null=True)
    iva = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='IVA')

    def __str__(self):
        return self.name

    def get_latitude(self):
        return self.coordinates.split(',')[0].replace(',', '.')

    def get_longitude(self):
        return self.coordinates.split(',')[1].replace(',', '.')

    def get_icon_image(self):
        if self.icon_image:
            return '{}{}'.format(settings.MEDIA_URL, self.icon_image)
        return '{}{}'.format(settings.STATIC_URL, 'img/default/empty.png')

    def remove_icon_image(self):
        try:
            if self.icon_image:
                os.remove(self.icon_image.path)
        except:
            pass

    class Meta:
        verbose_name = 'Página Principal'
        verbose_name_plural = 'Paginas Principales'
        default_permissions = ()
        permissions = (
            ('view_mainpage', 'Can view Página Principal'),
        )
        ordering = ['-id']


class Services(models.Model):
    name = models.CharField(max_length=150, verbose_name='Título')
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')
    image = models.ImageField(upload_to='services/%Y/%m/%d', verbose_name='Imagen', null=True, blank=True)
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.name

    def get_image(self):
        if self.image:
            return '{}{}'.format(settings.MEDIA_URL, self.image)
        return '{}{}'.format(settings.STATIC_URL, 'img/default/empty.png')

    def toJSON(self):
        item = model_to_dict(self)
        item['image'] = self.get_image()
        return item

    def delete(self, using=None, keep_parents=False):
        try:
            os.remove(self.image.path)
        except:
            pass
        super(Services, self).delete()

    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'
        ordering = ['-id']


class Departments(models.Model):
    name = models.CharField(max_length=150, verbose_name='Título')
    title = models.CharField(max_length=150, verbose_name='Subtítulo')
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')
    image = models.ImageField(upload_to='departments/%Y/%m/%d', verbose_name='Imagen', null=True, blank=True)
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.name

    def get_image(self):
        if self.image:
            return '{}{}'.format(settings.MEDIA_URL, self.image)
        return '{}{}'.format(settings.STATIC_URL, 'img/default/empty.png')

    def toJSON(self):
        item = model_to_dict(self)
        item['image'] = self.get_image()
        return item

    def delete(self, using=None, keep_parents=False):
        try:
            os.remove(self.image.path)
        except:
            pass
        super(Departments, self).delete()

    class Meta:
        verbose_name = 'Departmento'
        verbose_name_plural = 'Departmentos'
        ordering = ['-id']


class FreqQuestions(models.Model):
    question = models.CharField(max_length=500, verbose_name='Pregunta')
    answer = models.TextField(verbose_name='Respuesta')
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'Preguntas Frecuente'
        verbose_name_plural = 'Preguntas Frecuentes'
        ordering = ['-id']


class Testimonials(models.Model):
    names = models.CharField(max_length=150, verbose_name='Nombre')
    job = models.CharField(max_length=150, verbose_name='Profesión')
    desc = models.CharField(max_length=5000, verbose_name='Descripción')
    image = models.ImageField(upload_to='testimonials/%Y/%m/%d', verbose_name='Imagen', null=True, blank=True)
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.names

    def delete(self, using=None, keep_parents=False):
        try:
            os.remove(self.image.path)
        except:
            pass
        super(Testimonials, self).delete()

    def get_image(self):
        if self.image:
            return '{}{}'.format(settings.MEDIA_URL, self.image)
        return '{}{}'.format(settings.STATIC_URL, 'img/default/empty.png')

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Testimonios'
        verbose_name_plural = 'Testimonio'
        ordering = ['-id']


class Gallery(models.Model):
    date_joined = models.DateField(default=datetime.now)
    name = models.CharField(max_length=150, verbose_name='Nombre')
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')
    image = models.ImageField(upload_to='gallery/%Y/%m/%d', verbose_name='Imagen', null=True, blank=True)
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.image.url

    def get_image(self):
        if self.image:
            return '{}{}'.format(settings.MEDIA_URL, self.image)
        return '{}{}'.format(settings.STATIC_URL, 'img/default/empty.png')

    def toJSON(self):
        item = model_to_dict(self)
        item['image'] = self.get_image()
        return item

    def delete(self, using=None, keep_parents=False):
        try:
            os.remove(self.image.path)
        except:
            pass
        super(Gallery, self).delete()

    class Meta:
        verbose_name = 'Galería'
        verbose_name_plural = 'Galerias'
        ordering = ['-id']


class Comments(models.Model):
    names = models.CharField(max_length=100, verbose_name='Nombres')
    email = models.CharField(max_length=150, verbose_name='Email')
    mobile = models.CharField(max_length=15, verbose_name='Teléfono')
    message = models.CharField(max_length=2000, verbose_name='Mensaje')

    def __str__(self):
        return self.message

    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'
        default_permissions = ()
        permissions = (
            ('view_comments', 'Can view Comentarios'),
            ('delete_comments', 'Can delete Comentarios'),
        )
        ordering = ['-id']


class SocialNetworks(models.Model):
    css = models.CharField(max_length=50, verbose_name='Nombre de la clase css')
    icon = models.CharField(max_length=100, verbose_name='Icono font-awesome')
    url = models.CharField(max_length=150, verbose_name='Enlace')
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.css

    def toJSON(self):
        item = model_to_dict(self)
        return item

    def get_icon(self):
        if self.icon:
            return self.icon
        return 'fa fa-times'

    class Meta:
        verbose_name = 'Red Social'
        verbose_name_plural = 'Redes Sociales'
        ordering = ['id']


class Statistics(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True, verbose_name='Nombre')
    image = models.ImageField(upload_to='services/%Y/%m/%d', verbose_name='Imagen', null=True, blank=True)
    cant = models.IntegerField(default=0, verbose_name='Cantidad')
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.name

    def get_image(self):
        if self.image:
            return '{}{}'.format(settings.MEDIA_URL, self.image)
        return '{}{}'.format(settings.STATIC_URL, 'img/default/empty.png')

    def toJSON(self):
        item = model_to_dict(self)
        item['image'] = self.get_image()
        return item

    def delete(self, using=None, keep_parents=False):
        try:
            os.remove(self.image.path)
        except:
            pass
        super(Statistics, self).delete()

    class Meta:
        verbose_name = 'Estadística'
        verbose_name_plural = 'Estadísticas'
        ordering = ['-id']


class Team(models.Model):
    names = models.CharField(max_length=150, verbose_name='Nombre')
    phrase = models.CharField(max_length=5000, verbose_name='Frase')
    job = models.CharField(max_length=150, verbose_name='Profesión')
    image = models.ImageField(upload_to='team/%Y/%m/%d', verbose_name='Imagen', null=True, blank=True)
    desc = models.CharField(max_length=5000, null=True, blank=True, verbose_name='Descripción')
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.names

    def toJSON(self):
        item = model_to_dict(self)
        return item

    def delete(self, using=None, keep_parents=False):
        try:
            os.remove(self.image.path)
        except:
            pass
        super(Team, self).delete()

    def get_image(self):
        if self.image:
            return '{}{}'.format(settings.MEDIA_URL, self.image)
        return '{}{}'.format(settings.STATIC_URL, 'img/default/empty.png')

    def short_name(self):
        names = self.names.split(' ')
        if len(names) == 4:
            return '{} {}'.format(names[0], names[3])
        return self.names

    class Meta:
        verbose_name = 'Equipo de Trabajo'
        verbose_name_plural = 'Equipos de Trabajo'
        ordering = ['-id']


class TeamSocialNet(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    icon = models.CharField(max_length=50)
    url = models.CharField(max_length=500)

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Equipo de Trabajo | RedSocial'
        verbose_name_plural = 'Equipos de Trabajo | RedSocial'
        default_permissions = ()
        ordering = ['-id']


class Qualities(models.Model):
    name = models.CharField(max_length=150, verbose_name='Título')
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')
    image = models.ImageField(upload_to='qualities/%Y/%m/%d', verbose_name='Imagen', null=True, blank=True)
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.name

    def get_image(self):
        if self.image:
            return '{}{}'.format(settings.MEDIA_URL, self.image)
        return '{}{}'.format(settings.STATIC_URL, 'img/default/empty.png')

    def toJSON(self):
        item = model_to_dict(self)
        item['image'] = self.get_image()
        return item

    def delete(self, using=None, keep_parents=False):
        try:
            os.remove(self.image.path)
        except:
            pass
        super(Qualities, self).delete()

    class Meta:
        verbose_name = 'Cualidad'
        verbose_name_plural = 'Cualidades'
        ordering = ['-id']


class News(models.Model):
    date_joined = models.DateField(default=datetime.now)
    title = models.CharField(max_length=250, verbose_name='Título')
    desc = models.CharField(max_length=5000, verbose_name='Descripción')
    image = models.ImageField(upload_to='news/%Y/%m/%d', verbose_name='Imagen')
    url = models.TextField(verbose_name='Enlace web')
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return str(self.title)

    def trim_desc(self):
        return self.desc[0:150]

    def url_short(self):
        return self.url[0:50]

    def get_image(self):
        if self.image:
            return '{}{}'.format(settings.MEDIA_URL, self.image)
        return '{}{}'.format(settings.STATIC_URL, 'img/default/empty.png')

    def delete(self, using=None, keep_parents=False):
        try:
            os.remove(self.image.path)
        except:
            pass
        super(News, self).delete()

    class Meta:
        verbose_name = 'Noticia'
        verbose_name_plural = 'Noticias'
        ordering = ['id']


class Videos(models.Model):
    date_joined = models.DateField(default=datetime.now)
    title = models.CharField(max_length=250, verbose_name='Título')
    url = models.CharField(max_length=5000, verbose_name='Enlace')
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'
        ordering = ['id']

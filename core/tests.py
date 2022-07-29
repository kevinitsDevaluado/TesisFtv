from config.wsgi import *
from core.clinic.models import *
from core.security.models import *
from django.contrib.auth.models import Permission
from core.user.models import *
from core.homepage.models import *

# dashboard
dashboard = Dashboard()
dashboard.name = 'Pegasus S.A.'
dashboard.system_name = 'Pegasus S.A.'
dashboard.icon = 'fas fa-paw'
dashboard.layout = 1
dashboard.card = 'card-primary'
dashboard.navbar = 'navbar-dark navbar-primary'
dashboard.brand_logo = ''
dashboard.sidebar = 'sidebar-dark-primary'
dashboard.save()

# Mainpage
mainpage = Mainpage()
mainpage.name = 'Veterinaria Patitas Ajenas'
mainpage.proprietor = 'William Jair Dávila Vargas'
mainpage.desc = 'Te ofrecemos el mejor servicio y las más avanzadas técnicas médicas y quirúrgicas para tu mascota.'
mainpage.with_us = 'Somos una empresa dedicada al cuidado de las mascotas, que lleva en el mercado desde el año 2006, trabajando en pro del bienestar de cada mascota.'
mainpage.mission = 'Ofrecer bienestar a cada una de nuestras mascotas, que sus familias entiendan los deberes y los derechos que tienen las mascotas desde el instante que entran a formar parte de sus vidas. Nuestro grupo de trabajo comparte valores y principios éticos de respeto, responsabilidad y compromiso, superándolas expectativas de nuestros clientes y entregando calidad y satisfacción en nuestros servicios.'
mainpage.vision = 'Ser una empresa sólida, líder en prestación de servicios médicos veterinarios de la mejor calidad y profesionalismo, con énfasis en animales de compañía. Nuestro compromiso social es mejorar la calidad de vida de las familias a través del cuidado de la salud de nuestros pacientes contando con excelente tecnología, un equipo médico altamente calificado con educación y capacidad continua.'
mainpage.about_us = 'Proporcionar a las mascotas una atención de calidad con productos y servicios integrales satisfaciendo las necesidades de nuestros clientes.'
mainpage.phone = '042977552'
mainpage.mobile = '0979014552'
mainpage.address = 'Av. De la Prensa N70-174 y Gustavo Lemos'
mainpage.email = 'williamjair94@hotmail.com'
mainpage.coordinates = '-2.1327665,-79.5912141'
mainpage.about_youtube = 'https://www.youtube.com/watch?v=jDDaplaOz7Q'
mainpage.horary = 'Lunes a Viernes de 10:30 AM - 17:00 PM'
mainpage.save()

SocialNetworks(css='twitter', url='https://twitter.com/', icon='fab fa-twitter', state=True).save()
SocialNetworks(css='facebook', url='https://facebook.com/', icon='fab fa-facebook-f', state=True).save()
SocialNetworks(css='instagram', url='https://instagram.com/', icon='fab fa-instagram', state=True).save()
SocialNetworks(css='skype', url='https://skype.com/', icon='fab fa-skype', state=True).save()
SocialNetworks(css='linkedin', url='https://linkedin.com/', icon='fab fa-linkedin-in', state=True).save()

# module type

module = Module()
module.name = 'Cambiar password'
module.url = '/user/update/password/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-key'
module.description = 'Permite cambiar tu password de tu cuenta'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.name = 'Editar perfil'
module.url = '/user/update/profile/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-user'
module.description = 'Permite cambiar la información de tu cuenta'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.name = 'Editar perfil'
module.url = '/clinic/client/update/profile/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-user'
module.description = 'Permite cambiar la información de tu cuenta'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.name = 'Editar perfil'
module.url = '/clinic/employee/update/profile/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-user'
module.description = 'Permite cambiar la información de tu cuenta'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.name = 'Mascotas'
module.url = '/clinic/mascots/client/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-bone'
module.description = 'Permite administrar las mascotas del sistema'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.name = 'Historial Médico'
module.url = '/clinic/historial/medical/client/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-first-aid'
module.description = 'Permite administrar los historiales medicos de las mascotas'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.name = 'Ventas'
module.url = '/clinic/sale/client/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-shopping-cart'
module.description = 'Permite administrar las ventas de la veterinaria'
module.save()
print('insertado {}'.format(module.name))

type = ModuleType()
type.name = 'Seguridad'
type.icon = 'fas fa-lock'
type.save()
print('insertado {}'.format(type.name))

module = Module()
module.moduletype_id = 1
module.name = 'Tipos de Módulos'
module.url = '/security/module/type/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-door-open'
module.description = 'Permite administrar los tipos de módulos del sistema'
module.save()
for p in Permission.objects.filter(content_type__model=ModuleType._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 1
module.name = 'Módulos'
module.url = '/security/module/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-th-large'
module.description = 'Permite administrar los módulos del sistema'
module.save()
for p in Permission.objects.filter(content_type__model=Module._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 1
module.name = 'Grupos'
module.url = '/security/group/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-users'
module.description = 'Permite administrar los grupos de usuarios del sistema'
module.save()
for p in Permission.objects.filter(content_type__model=Group._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 1
module.name = 'Respaldos'
module.url = '/security/database/backups/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-database'
module.description = 'Permite administrar los respaldos de base de datos'
module.save()
for p in Permission.objects.filter(content_type__model=DatabaseBackups._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 1
module.name = 'Conf. Dashboard'
module.url = '/security/dashboard/update/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-tools'
module.description = 'Permite configurar los datos de la plantilla'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 1
module.name = 'Accesos'
module.url = '/security/access/users/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-user-secret'
module.description = 'Permite administrar los accesos de los usuarios'
module.save()
for p in Permission.objects.filter(content_type__model=AccessUsers._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

type = ModuleType()
type.name = 'Usuarios'
type.icon = 'fas fa-users'
type.save()
print('insertado {}'.format(type.name))

module = Module()
module.moduletype_id = 2
module.name = 'Administradores'
module.url = '/user/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-user'
module.description = 'Permite administrar a los administradores del sistema'
module.save()
for p in Permission.objects.filter(content_type__model=User._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 2
module.name = 'Profesiones'
module.url = '/clinic/profession/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-user-md'
module.description = 'Permite administrar las profesiones de los empleados'
module.save()
for p in Permission.objects.filter(content_type__model=Profession._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

type = ModuleType()
type.name = 'Página Web'
type.icon = 'fas fa-house-damage'
type.save()
print('insertado {}'.format(type.name))

module = Module()
module.moduletype_id = 3
module.name = 'Información'
module.url = '/mainpage/update/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-home'
module.description = 'Permite administrar la información de la página principal'
module.save()
for p in Permission.objects.filter(content_type__model=Mainpage._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 3
module.name = 'Noticias'
module.url = '/homepage/news/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'far fa-newspaper'
module.description = 'Permite administrar las noticias del dashboard'
module.save()
for p in Permission.objects.filter(content_type__model=News._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 3
module.name = 'Videos'
module.url = '/homepage/videos/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-photo-video'
module.description = 'Permite administrar las videos del dashboard'
module.save()
for p in Permission.objects.filter(content_type__model=Videos._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 3
module.name = 'Redes Sociales'
module.url = '/homepage/socialnetworks/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'far fa-thumbs-up'
module.description = 'Permite administrar las redes sociales de la página'
module.save()
for p in Permission.objects.filter(content_type__model=SocialNetworks._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 3
module.name = 'Departamentos'
module.url = '/homepage/departments/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-city'
module.description = 'Permite administrar los departamentos de la página'
module.save()
for p in Permission.objects.filter(content_type__model=Departments._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 3
module.name = 'Servicios'
module.url = '/homepage/services/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-atlas'
module.description = 'Permite administrar los servicios de la página'
module.save()
for p in Permission.objects.filter(content_type__model=Services._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 3
module.name = 'Estadísticas'
module.url = '/homepage/statistics/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fab fa-stack-overflow'
module.description = 'Permite administrar las estadísticas de la página'
module.save()
for p in Permission.objects.filter(content_type__model=Statistics._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 3
module.name = 'Preguntas frecuentes'
module.url = '/homepage/freqquestions/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-question-circle'
module.description = 'Permite administrar las preguntas frecuentes de la página'
module.save()
for p in Permission.objects.filter(content_type__model=FreqQuestions._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 3
module.name = 'Testimonios'
module.url = '/homepage/testimonials/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-comment-alt'
module.description = 'Permite administrar los testimonios de la página'
module.save()
for p in Permission.objects.filter(content_type__model=Testimonials._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 3
module.name = 'Galería'
module.url = '/homepage/gallery/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-file-image'
module.description = 'Permite administrar las imágenes de la página'
module.save()
for p in Permission.objects.filter(content_type__model=Gallery._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 3
module.name = 'Doctores'
module.url = '/homepage/team/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-users-cog'
module.description = 'Permite administrar a los doctores de la página'
module.save()
for p in Permission.objects.filter(content_type__model=Team._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 3
module.name = 'Comentarios'
module.url = '/homepage/comments/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-envelope'
module.description = 'Permite administrar los comentarios de la página'
module.save()
for p in Permission.objects.filter(content_type__model=Comments._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 3
module.name = 'Cualidades'
module.url = '/homepage/qualities/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-folder-open'
module.description = 'Permite administrar los comentarios de la página'
module.save()
for p in Permission.objects.filter(content_type__model=Qualities._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

type = ModuleType()
type.name = 'Veterinaria'
type.icon = 'fas fa-hospital'
type.save()
print('insertado {}'.format(type.name))

module = Module()
module.moduletype_id = 4
module.name = 'Clientes'
module.url = '/clinic/client/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-male'
module.description = 'Permite administrar a los clientes del sistema'
module.save()
for p in Permission.objects.filter(content_type__model=Client._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 4
module.name = 'Parámetros Médicos'
module.url = '/clinic/medical/parameters/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-mortar-pestle'
module.description = 'Permite administrar los parámetros médicos del sistema'
module.save()
for p in Permission.objects.filter(content_type__model=MedicalParameters._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 4
module.name = 'Tipos'
module.url = '/clinic/type/pet/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-folder'
module.description = 'Permite administrar a los tipos de animales del sistema'
module.save()
for p in Permission.objects.filter(content_type__model=TypePet._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 4
module.name = 'Razas'
module.url = '/clinic/breed/pet/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-folder-open'
module.description = 'Permite administrar las razas de las mascotas del sistema'
module.save()
for p in Permission.objects.filter(content_type__model=BreedPet._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 4
module.name = 'Mascotas'
module.url = '/clinic/mascots/admin/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-bone'
module.description = 'Permite administrar las mascotas del sistema'
module.save()
for p in Permission.objects.filter(content_type__model=Mascots._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 4
module.name = 'Historial Médico'
module.url = '/clinic/historial/medical/admin/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-first-aid'
module.description = 'Permite administrar los historiales medicos de las mascotas'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 4
module.name = 'Colores'
module.url = '/clinic/color/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-file-medical'
module.description = 'Permite administrar los colores del sistema'
module.save()
for p in Permission.objects.filter(content_type__model=Color._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 4
module.name = 'Ventas'
module.url = '/clinic/sale/admin/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-shopping-cart'
module.description = 'Permite administrar las ventas de la veterinaria'
module.save()
for p in Permission.objects.filter(content_type__model=Sale._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.name = 'Ventas'
module.url = '/clinic/sale/employee/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-shopping-cart'
module.description = 'Permite administrar las ventas de la veterinaria'
module.save()
for p in Permission.objects.filter(content_type__model=Sale._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

type = ModuleType()
type.name = 'Bodega'
type.icon = 'fas fa-boxes'
type.save()
print('insertado {}'.format(type.name))

module = Module()
module.moduletype_id = 5
module.name = 'Proveedores'
module.url = '/clinic/provider/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-truck-loading'
module.description = 'Permite administrar a los proveedores para las compras'
module.save()
for p in Permission.objects.filter(content_type__model=Provider._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 5
module.name = 'Tipos de Productos'
module.url = '/erp/product/type/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fab fa-linode'
module.description = 'Permite administrar la linea de los productos'
module.save()
for p in Permission.objects.filter(content_type__model=ProductType._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 5
module.name = 'Productos'
module.url = '/clinic/product/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-box-open'
module.description = 'Permite administrar los productos del sistema'
module.save()
for p in Permission.objects.filter(content_type__model=Product._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 5
module.name = 'Compras'
module.url = '/clinic/purchase/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-vote-yea'
module.description = 'Permite administrar las compras del sistema'
module.save()
for p in Permission.objects.filter(content_type__model=Purchase._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

type = ModuleType()
type.name = 'Reportes'
type.icon = 'fas fa-chart-pie'
type.save()
print('insertado {}'.format(type.name))

module = Module()
module.moduletype_id = 6
module.name = 'Ventas'
module.url = '/reports/sale/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los reportes de las ventas'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 6
module.name = 'Compras'
module.url = '/reports/purchase/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los reportes de las compras'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 6
module.name = 'Historiales Médicos'
module.url = '/reports/historial/medical/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los reportes de los historiales médicos'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 6
module.name = 'Reporte de Clientes'
module.url = '/reports/client/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los reportes de los clientes'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 6
module.name = 'Reporte de Mascotas'
module.url = '/reports/mascots/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los reportes de los clientes'
module.save()
print('insertado {}'.format(module.name))

type = ModuleType()
type.name = 'Ubicación'
type.icon = 'fas fa-street-view'
type.save()
print('insertado {}'.format(type.name))

module = Module()
module.moduletype_id = 7
module.name = 'Paises'
module.url = '/clinic/country/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-globe-europe'
module.description = 'Permite administrar los paises'
module.save()
for p in Permission.objects.filter(content_type__model=Country._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 7
module.name = 'Provincias'
module.url = '/clinic/province/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-globe'
module.description = 'Permite administrar las provincias del sistema'
module.save()
for p in Permission.objects.filter(content_type__model=Province._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 7
module.name = 'Cantones'
module.url = '/clinic/canton/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-globe-americas'
module.description = 'Permite administrar los cantones del sistema'
module.save()
for p in Permission.objects.filter(content_type__model=Canton._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 7
module.name = 'Parroquias'
module.url = '/clinic/parish/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-search-location'
module.description = 'Permite administrar las parroquias del sistema'
module.save()
for p in Permission.objects.filter(content_type__model=Parish._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 2
module.name = 'Empleados'
module.url = '/clinic/employee/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-male'
module.description = 'Permite administrar a los empleados del sistema'
module.save()
for p in Permission.objects.filter(content_type__model=Employee._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

# group
group = Group()
group.name = 'Administrador'
group.save()
print('insertado {}'.format(group.name))
notsearch = [
    '/clinic/mascots/client/',
    '/clinic/historial/medical/client/',
    '/clinic/sale/client/',
    '/clinic/sale/employee/',
    '/clinic/client/update/profile/',
    '/clinic/employee/update/profile/',
]
for m in Module.objects.filter().exclude(
        url__in=notsearch):
    gm = GroupModule()
    gm.module = m
    gm.group = group
    gm.save()
    for perm in m.permits.all():
        group.permissions.add(perm)
        grouppermission = GroupPermission()
        grouppermission.module_id = m.id
        grouppermission.group_id = group.id
        grouppermission.permission_id = perm.id
        grouppermission.save()

# client
group = Group()
group.name = 'Cliente'
group.save()
print('insertado {}'.format(group.name))
search = [
    '/clinic/mascots/client/',
    '/user/update/password/',
    '/clinic/historial/medical/client/',
    '/clinic/sale/client/',
    '/clinic/client/update/profile/',
]
for m in Module.objects.filter(url__in=search):
    gm = GroupModule()
    gm.module = m
    gm.group = group
    gm.save()

group = Group()
group.name = 'Empleado'
group.save()
print('insertado {}'.format(group.name))
search = [
    '/clinic/sale/employee/',
    '/user/update/password/',
    '/clinic/employee/update/profile/',
]
for m in Module.objects.filter(url__in=search):
    gm = GroupModule()
    gm.module = m
    gm.group = group
    gm.save()

# user
u = User()
u.first_name = 'William Dávila'
u.last_name = 'Dávila Vargas'
u.username = '0928363993'
u.dni = '0928363993'
u.email = 'davilawilliam93@gmail.com'
u.is_active = True
u.is_superuser = True
u.is_staff = True
u.set_password('hacker94')
u.save()

group = Group.objects.get(pk=1)
u.groups.add(group)

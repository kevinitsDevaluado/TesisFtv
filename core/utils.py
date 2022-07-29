from config import wsgi
import json
from random import randint

from django.db.models import Q

from core.clinic.models import *
from core.security.models import Module

src = '../deploy/censos.csv'


def load_province():
    try:
        file = open(src, 'r', encoding="utf8")
        for c in file.readlines():
            data = c.strip().split(',')
            if not Province.objects.filter(code=data[0]).exists():
                province = Province()
                province.country_id = 58
                province.name = data[1]
                province.code = data[0]
                province.save()
    except Exception as e:
        print(e)
    finally:
        load_canton()


def load_canton():
    try:
        file = open(src, 'r', encoding="utf8")
        for c in file.readlines():
            data = c.strip().split(',')
            code = data[0]
            name = data[2]
            if not Canton.objects.filter(province__code=code, name=name).exists():
                canton = Canton()
                canton.name = name
                canton.province = Province.objects.get(code=code)
                canton.save()
                print(canton.name)

    except Exception as e:
        print(e)
    finally:
        load_parish()


def load_parish():
    try:
        file = open(src, 'r', encoding="utf8")
        for c in file.readlines():
            data = c.strip().split(',')
            province = Province.objects.get(code=data[0])
            canton = Canton.objects.get(name=data[2], province_id=province.id)
            if not Parish.objects.filter(name=data[3], canton_id=canton).exists():
                parish = Parish()
                parish.canton_id = canton.id
                parish.name = data[3]
                parish.save()
                print(canton.name)
    except Exception as e:
        print(e)


def load_country():
    try:
        file = open('../deploy/country.txt', 'r', encoding="utf8")
        for c in file.readlines():
            line = c.strip().split(',')
            b = Country()
            b.code = line[0]
            b.name = line[1]
            b.save()
            print(b.name)
    except Exception as e:
        print(e)
    finally:
        load_province()


def get_google_translate(text=''):
    from googletrans import Translator
    translator = Translator()
    translations = translator.translate(text, dest='es')
    return translations.text


def load_colors():
    with open('../deploy/colors.json', encoding="utf8") as f:
        data = json.load(f)
        for p in data:
            try:
                name = p['name']
                hex = p['hex']
                if not Color.objects.filter(Q(hex=hex) | Q(name=name)).exists():
                    c = Color()
                    c.name = get_google_translate(name)
                    c.hex = hex
                    c.save()
                    print(c.name)
            except Exception as e:
                print(e)


def load_archive():
    try:
        file = open('clinic.txt', 'r', encoding="utf8")
        for c in file.readlines():
            name = c.strip()
            p = Product()
            p.name = name
            p.price = randint(2, 50)
            p.producttype_id = randint(1, 3)
            p.save()
            print(name)
    except Exception as e:
        print(e)


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

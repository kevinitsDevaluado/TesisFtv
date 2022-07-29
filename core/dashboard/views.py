import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, FloatField
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import requires_csrf_token
from django.views.generic import TemplateView

from core.clinic.models import Provider, Mascots, Product, SaleProducts, Sale, type_sale
from core.homepage.models import *
from core.reports.choices import months
from core.security.models import Dashboard
from core.user.models import User


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'panel.html'

    def get_graph_sales_products_year_month(self):
        data = []
        year = datetime.now().year
        month = datetime.now().month
        try:
            for p in Product.objects.all():
                total = SaleProducts.objects.filter(sale__date_joined__year=year, sale__date_joined__month=month,
                                                    product_id=p.id, product__producttype__has_stock=True).aggregate(
                    r=Coalesce(Sum('subtotal'), 0.00, output_field=FloatField())).get('r')
                if total > 0:
                    data.append({
                        'name': p.name,
                        'y': float(total)
                    })
        except:
            pass
        return data

    def get_graph_sales_year_month(self):
        data = []
        try:
            year = datetime.now().year
            for m in range(1, 13):
                total = Sale.objects.filter(date_joined__year=year, date_joined__month=m).aggregate(
                    r=Coalesce(Sum('total'), 0.00, output_field=FloatField())).get('r')
                data.append(float(total))
        except:
            pass
        return data

    def get_graph_sales_category(self):
        data = []
        try:
            datenow = datetime.now()
            for m in type_sale[1:]:
                total = Sale.objects.filter(date_joined__year=datenow.year, date_joined__month=datenow.month,
                                            type=m[0]).aggregate(r=Coalesce(Sum('total'), 0.00, output_field=FloatField())).get('r')
                data.append({
                    'name': m[1],
                    'y': float(total)
                })
        except:
            pass
        return data

    def get(self, request, *args, **kwargs):
        request.user.set_group_session()
        context = self.get_context_data()
        dashboard = Dashboard.objects.filter()
        if dashboard.exists():
            if dashboard[0].layout == 1:
                if self.request.user.get_group_id_session() == 1:
                    context['clients'] = User.objects.filter(groups__in=[settings.GROUPS.get('client')]).count()
                    context['provider'] = Provider.objects.all().count()
                    context['mascots'] = Mascots.objects.all().count()
                    context['products'] = Product.objects.all().count()
                    context['datenow'] = datetime.now().date()
                    context['month'] = months[datetime.now().date().month][1]
                else:
                    context['videos'] = Videos.objects.filter(state=True)
                    context['news'] = News.objects.filter(state=True)
                return render(request, 'vtcpanel.html', context)
        return render(request, 'hztpanel.html', context)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'get_graph_sales_products_year_month':
                data = {
                    'name': 'Porcentaje',
                    'colorByPoint': True,
                    'data': self.get_graph_sales_products_year_month(),
                }
            elif action == 'get_graph_sales_year_month':
                data = {
                    'name': 'Porcentaje de venta',
                    'showInLegend': False,
                    'colorByPoint': True,
                    'data': self.get_graph_sales_year_month()
                }
            elif action == 'get_graph_sales_category':
                data = {
                    'name': 'Porcentaje',
                    'colorByPoint': True,
                    'data': self.get_graph_sales_category(),
                }
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Panel de administración'
        return context


@requires_csrf_token
def error_404(request, exception):
    return render(request, '404.html', {})


@requires_csrf_token
def error_500(request, exception):
    return render(request, '500.html', {})

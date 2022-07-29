from django.urls import path

from .views.client_report.views import ClientReportView
from .views.historialmedical_report.views import HistorialMedicalReportView
from .views.purchase_report.views import PurchaseReportView
from .views.sale_report.views import SaleReportView
from .views.mascots_report.views import MascotsReportView

urlpatterns = [
    path('sale/', SaleReportView.as_view(), name='sale_report'),
    path('purchase/', PurchaseReportView.as_view(), name='purchase_report'),
    path('historial/medical/', HistorialMedicalReportView.as_view(), name='historial_medical_report'),
    path('client/', ClientReportView.as_view(), name='client_report'),
    path('mascots/', MascotsReportView.as_view(), name='mascots_report'),
]

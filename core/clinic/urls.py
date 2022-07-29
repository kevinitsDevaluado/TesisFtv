from django.urls import path

from .views.historialmedical.admin.views import HistorialMedicalAdminListView
from .views.historialmedical.client.views import HistorialMedicalClientListView
from .views.medicalparameters.views import *
from .views.producttype.views import *
from .views.profession.views import *
from .views.provider.views import *
from .views.product.views import *
from .views.province.views import *
from .views.country.views import *
from .views.parish.views import *
from .views.canton.views import *
from .views.purchase.views import *
from .views.client.views import *
from .views.sale.client.views import *
from .views.typepet.views import *
from .views.breedpet.views import *
from .views.employee.views import *
from .views.color.views import *
from .views.mascots.admin.views import *
from .views.mascots.client.views import *
from .views.sale.admin.views import *
from .views.sale.print.views import *
from .views.sale.employee.views import *

urlpatterns = [
    # profession
    path('profession/', ProfessionListView.as_view(), name='profession_list'),
    path('profession/add/', ProfessionCreateView.as_view(), name='profession_create'),
    path('profession/update/<int:pk>/', ProfessionUpdateView.as_view(), name='profession_update'),
    path('profession/delete/<int:pk>/', ProfessionDeleteView.as_view(), name='profession_delete'),
    # province
    path('province/', ProvinceListView.as_view(), name='province_list'),
    path('province/add/', ProvinceCreateView.as_view(), name='province_create'),
    path('province/update/<int:pk>/', ProvinceUpdateView.as_view(), name='province_update'),
    path('province/delete/<int:pk>/', ProvinceDeleteView.as_view(), name='province_delete'),
    # canton
    path('canton/', CantonListView.as_view(), name='canton_list'),
    path('canton/add/', CantonCreateView.as_view(), name='canton_create'),
    path('canton/update/<int:pk>/', CantonUpdateView.as_view(), name='canton_update'),
    path('canton/delete/<int:pk>/', CantonDeleteView.as_view(), name='canton_delete'),
    # parish
    path('parish/', ParishListView.as_view(), name='parish_list'),
    path('parish/add/', ParishCreateView.as_view(), name='parish_create'),
    path('parish/update/<int:pk>/', ParishUpdateView.as_view(), name='parish_update'),
    path('parish/delete/<int:pk>/', ParishDeleteView.as_view(), name='parish_delete'),
    # country
    path('country/', CountryListView.as_view(), name='country_list'),
    path('country/add/', CountryCreateView.as_view(), name='country_create'),
    path('country/update/<int:pk>/', CountryUpdateView.as_view(), name='country_update'),
    path('country/delete/<int:pk>/', CountryDeleteView.as_view(), name='country_delete'),
    # provider
    path('provider/', ProviderListView.as_view(), name='provider_list'),
    path('provider/add/', ProviderCreateView.as_view(), name='provider_create'),
    path('provider/update/<int:pk>/', ProviderUpdateView.as_view(), name='provider_update'),
    path('provider/delete/<int:pk>/', ProviderDeleteView.as_view(), name='provider_delete'),
    # producttype
    path('product/type/', ProductTypeListView.as_view(), name='producttype_list'),
    path('product/type/add/', ProductTypeCreateView.as_view(), name='producttype_create'),
    path('product/type/update/<int:pk>/', ProductTypeUpdateView.as_view(), name='producttype_update'),
    path('product/type/delete/<int:pk>/', ProductTypeDeleteView.as_view(), name='producttype_delete'),
    # product
    path('product/', ProductListView.as_view(), name='product_list'),
    path('product/add/', ProductCreateView.as_view(), name='product_create'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    # purchases
    path('purchase/', PurchaseListView.as_view(), name='purchase_list'),
    path('purchase/add/', PurchaseCreateView.as_view(), name='purchase_create'),
    path('purchase/delete/<int:pk>/', PurchaseDeleteView.as_view(), name='purchase_delete'),
    # clients
    path('client/', ClientListView.as_view(), name='client_list'),
    path('client/add/', ClientCreateView.as_view(), name='client_create'),
    path('client/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    path('client/update/profile/', ClientUpdateProfileView.as_view(), name='client_update_profile'),
    # employees
    path('employee/', EmployeeListView.as_view(), name='employee_list'),
    path('employee/add/', EmployeeCreateView.as_view(), name='employee_create'),
    path('employee/update/<int:pk>/', EmployeeUpdateView.as_view(), name='employee_update'),
    path('employee/delete/<int:pk>/', EmployeeDeleteView.as_view(), name='employee_delete'),
    path('employee/update/profile/', EmployeeUpdateProfileView.as_view(), name='employee_update_profile'),
    # typepet
    path('type/pet/', TypePetListView.as_view(), name='typepet_list'),
    path('type/pet/add/', TypePetCreateView.as_view(), name='typepet_create'),
    path('type/pet/update/<int:pk>/', TypePetUpdateView.as_view(), name='typepet_update'),
    path('type/pet/delete/<int:pk>/', TypePetDeleteView.as_view(), name='typepet_delete'),
    # breedpet
    path('breed/pet/', BreedPetListView.as_view(), name='breedpet_list'),
    path('breed/pet/add/', BreedPetCreateView.as_view(), name='breedpet_create'),
    path('breed/pet/update/<int:pk>/', BreedPetUpdateView.as_view(), name='breedpet_update'),
    path('breed/pet/delete/<int:pk>/', BreedPetDeleteView.as_view(), name='breedpet_delete'),
    # mascots/admin
    path('mascots/admin/', MascotsAdminListView.as_view(), name='mascots_admin_list'),
    path('mascots/admin/add/', MascotsAdminCreateView.as_view(), name='mascots_admin_create'),
    path('mascots/admin/update/<int:pk>/', MascotsAdminUpdateView.as_view(), name='mascots_admin_update'),
    path('mascots/admin/delete/<int:pk>/', MascotsAdminDeleteView.as_view(), name='mascots_admin_delete'),
    # mascots/client
    path('mascots/client/', MascotsClientListView.as_view(), name='mascots_client_list'),
    path('mascots/client/add/', MascotsClientCreateView.as_view(), name='mascots_client_create'),
    path('mascots/client/update/<int:pk>/', MascotsClientUpdateView.as_view(), name='mascots_client_update'),
    path('mascots/client/delete/<int:pk>/', MascotsClientDeleteView.as_view(), name='mascots_client_delete'),
    # color
    path('color/', ColorListView.as_view(), name='color_list'),
    path('color/add/', ColorCreateView.as_view(), name='color_create'),
    path('color/update/<int:pk>/', ColorUpdateView.as_view(), name='color_update'),
    path('color/delete/<int:pk>/', ColorDeleteView.as_view(), name='color_delete'),
    # medical parameters
    path('medical/parameters/', MedicalParametersListView.as_view(), name='medicalparameters_list'),
    path('medical/parameters/add/', MedicalParametersCreateView.as_view(), name='medicalparameters_create'),
    path('medical/parameters/update/<int:pk>/', MedicalParametersUpdateView.as_view(), name='medicalparameters_update'),
    path('medical/parameters/delete/<int:pk>/', MedicalParametersDeleteView.as_view(), name='medicalparameters_delete'),
    # sale/admin
    path('sale/admin/', SaleAdminListView.as_view(), name='sale_admin_list'),
    path('sale/admin/delete/<int:pk>/', SaleAdminDeleteView.as_view(), name='sale_admin_delete'),
    # sale/employee
    path('sale/employee/', SaleEmployeeListView.as_view(), name='sale_employee_list'),
    path('sale/employee/add/', SaleEmployeeCreateView.as_view(), name='sale_employee_create'),
    path('sale/employee/delete/<int:pk>/', SaleEmployeeDeleteView.as_view(), name='sale_employee_delete'),
    path('sale/employee/attend/<int:pk>/', SaleEmployeeAttendView.as_view(), name='sale_employee_attend'),
    # sale/client
    path('sale/client/', SaleClientListView.as_view(), name='sale_client_list'),
    path('sale/client/add/', SaleClienCreateView.as_view(), name='sale_client_create'),
    # sale/print
    path('sale/print/voucher/<int:pk>/', SalePrintVoucherView.as_view(), name='sale_print_voucher'),
    # historial medical
    path('historial/medical/admin/', HistorialMedicalAdminListView.as_view(), name='historial_medical_admin_list'),
    path('historial/medical/client/', HistorialMedicalClientListView.as_view(), name='historial_medical_client_list'),
]

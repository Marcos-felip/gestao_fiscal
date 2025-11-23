from django.urls import path
from partners.views import customers, suppliers

app_name = 'partners'

urlpatterns = [
    path('customers/', customers.CustomerListView.as_view(), name='customer_list'),
    path('customers/create/', customers.CustomerTemplateView.as_view(), name='customer_base'),
    path('customers/create/basic/', customers.CustomerBasicCreateView.as_view(), name='customer_create_basic'),
    path('customers/<int:pk>/edit/', customers.CustomerUpdateView.as_view(), name='customer_update'),
    path('customers/<int:pk>/edit/advanced/', customers.CustomerAdvancedUpdateView.as_view(), name='customer_advanced'),
    path('customers/<int:pk>/edit/address/', customers.CustomerAddressUpdateView.as_view(), name='customer_address'),

    path('suppliers/', suppliers.SupplierListView.as_view(), name='supplier_list'),
    path('suppliers/create/', suppliers.SupplierTemplateView.as_view(), name='supplier_base'),
    path('suppliers/create/basic/', suppliers.SupplierBasicCreateView.as_view(), name='supplier_create_basic'),
    path('suppliers/<int:pk>/edit/', suppliers.SupplierUpdateView.as_view(), name='supplier_update'),
    path('suppliers/<int:pk>/edit/advanced/', suppliers.SupplierAdvancedUpdateView.as_view(), name='supplier_advanced'),
    path('suppliers/<int:pk>/edit/address/', suppliers.SupplierAddressUpdateView.as_view(), name='supplier_address'),
    
]
from django.urls import path
from partners.views import customers

app_name = 'partners'

urlpatterns = [
    path('customers/', customers.CustomerListView.as_view(), name='customer_list'),
]
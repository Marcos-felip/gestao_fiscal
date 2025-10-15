from django.contrib import admin

from partners.models.customers import Customer
from partners.models.suppliers import Supplier

admin.site.register(Customer)
admin.site.register(Supplier)
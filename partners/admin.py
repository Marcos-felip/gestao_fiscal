from django.contrib import admin

from partners.models.customer import Customer
from partners.models.supplier import Supplier

admin.site.register(Customer)
admin.site.register(Supplier)
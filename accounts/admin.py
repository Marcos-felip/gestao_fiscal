from django.contrib import admin
from accounts.models.user import User, Membership
from accounts.models.company import Company, Establishment
from accounts.models.address import Address

# Register your models here.
admin.site.register(User)
admin.site.register(Membership)
admin.site.register(Company)
admin.site.register(Establishment)
admin.site.register(Address)

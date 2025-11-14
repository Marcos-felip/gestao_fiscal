from django.contrib import admin
from accounts.models.user import User, Membership, Permission
from accounts.models.company import Company, Establishment

# Register your models here.
admin.site.register(User)
admin.site.register(Membership)
admin.site.register(Permission)
admin.site.register(Company)
admin.site.register(Establishment)

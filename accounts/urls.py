from django.urls import path
from django.contrib.auth.decorators import login_required

from accounts.views import company

app_name = 'accounts'

urlpatterns = [
    path('company/create/', login_required(company.CompanyCreateView.as_view()), name='company_create'),
]

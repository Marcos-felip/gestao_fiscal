from django.urls import path
from django.contrib.auth.decorators import login_required

from accounts.views.company import CompanyCreateView

app_name = 'accounts'

urlpatterns = [
    path('company/create/', login_required(CompanyCreateView.as_view()), name='company_create'),
]

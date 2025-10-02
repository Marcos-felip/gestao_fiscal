from django.urls import path
from django.contrib.auth.decorators import login_required
from dashboard.views import home

app_name = 'dashboard'

urlpatterns = [
    path('', login_required(home.HomeView.as_view()), name='home'),
]
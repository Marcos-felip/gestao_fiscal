from django.urls import path
from django.contrib.auth.decorators import login_required
from dashboard.views import home, users, company

app_name = 'dashboard'

urlpatterns = [
    path('', login_required(home.HomeView.as_view()), name='home'),
    path('users/', login_required(users.UserListView.as_view()), name='user_list'),
    path('users/create/', login_required(users.UserCreateView.as_view()), name='user_create'),
    path('users/<int:pk>/update/', login_required(users.UserUpdateView.as_view()), name='user_update'),
    path('users/<int:pk>/delete/', login_required(users.UserDeleteView.as_view()), name='user_delete'),
    path('company/<int:pk>/update/', login_required(company.CompanyUpdateView.as_view()), name='company_update'),
]
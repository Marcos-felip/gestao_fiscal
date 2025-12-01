from django.urls import path
from inventory.views import category, unit

app_name = 'inventory'

urlpatterns = [
    path('categories/', category.CategoryListView.as_view(), name='category_list'),
    path('categories/create/', category.CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/update/', category.CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', category.CategoryDeleteView.as_view(), name='category_delete'),

    path('units/', unit.UnitListView.as_view(), name='unit_list'),
    path('units/create/', unit.UnitCreateView.as_view(), name='unit_create'),
    path('units/<int:pk>/update/', unit.UnitUpdateView.as_view(), name='unit_update'),
    path('units/<int:pk>/delete/', unit.UnitDeleteView.as_view(), name='unit_delete'),
]
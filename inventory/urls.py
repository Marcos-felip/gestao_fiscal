from django.urls import path
from inventory.views import category

app_name = 'inventory'

urlpatterns = [
    path('categories/', category.CategoryListView.as_view(), name='category_list'),
    path('categories/create/', category.CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/update/', category.CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', category.CategoryDeleteView.as_view(), name='category_delete'),
]
from django.urls import path

from .views import ProductDetailView, ProductListView

urlpatterns = [
    path('product/', ProductListView.as_view(), name='product'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_update'),
]
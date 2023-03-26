from django.urls import path
from . import views


urlpatterns = [
    # products
    path('products/', views.ProductView.as_view(), name='products'),
    path('products/<int:pk>/', views.ProductView.as_view(), name='products-detail'),

    # categories
    path('categories/', views.CategoryView.as_view(), name='categories'),
    path('categories/<int:pk>/', views.CategoryView.as_view(), name='categories-detail')
]


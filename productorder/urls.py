from django.urls import path
from . import views


urlpatterns = [
    # cart
    path('cart/', views.CartView.as_view(), name='cart' ),

    # orders
    path('orders/<int:id>/', views.OrdersView.as_view()),
    path('orders/', views.OrdersView.as_view(), name='orders' ),

    # checkout
    path('checkout/<int:id>/', views.CheckoutView.as_view(), name='checkout'),
    path('create-checkout-session', views.PaymentView.as_view(),
         name='payment')


    ]

from django.urls import path
from . import views


urlpatterns = [
    # products
    path('user/', views.UserView.as_view(), name='user')
]


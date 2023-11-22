from django.urls import path
from .views import pay, ipn, success

app_name = 'payment_gateway'

urlpatterns = [
    path('', pay, name='pay'),
    path('ipn/', ipn),
    path('success/', success)
]

from django.urls import path
from .views import payment_link_view, pay

app_name = 'payment_gateway'

urlpatterns = [
    path('', pay, name='pay'),
    path('pay-with-yenepay/', payment_link_view, name='payment_link'),
]

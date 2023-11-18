from django.urls import path
from . import views


urlpatterns = [
	path('', views.index, name='index'),
	path('booking/<str:code>', views.booking, name='booking'),
	path('scheduled', views.scheduled, name='scheduled'),
	path('delete_booking/<str:code>', views.delete_booking, name='delete-booking')
]

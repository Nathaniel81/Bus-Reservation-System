from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'core'

urlpatterns = [
	path('', views.index, name='index'),
	path('booking/<str:code>', views.booking, name='booking'),
	path('scheduled', views.scheduled, name='scheduled'),
	path('delete_booking/<str:code>', views.delete_booking, name='delete-booking'),
	path('find_trip/', views.find_trip, name='find-trip'),
	path('searched_trip/', views.searched_trip, name='searched_trip'),
	path('logout/', LogoutView.as_view(), name='logout'),
]

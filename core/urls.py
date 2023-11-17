from django.urls import path
from . import views


urlpatterns = [
	path('', views.index, name='index'),
	path('booking/<str:code>', views.booking, name='booking'),
	path('detail/<str:code>', views.detail, name='detail')
]

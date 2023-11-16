from django.shortcuts import render
from django.db.models import Q
from .models import *


def index(request):
    context = {}
    query = request.GET.get('query', '')
    if query:
        context['schedules'] = Schedule.objects.filter(
			Q(departure__name__icontains=query)|
			Q(destination__name__icontains=query)|
			Q(bus__name__icontains=query)|
			Q(bus__driver__icontains=query)
		).distinct()
    else:
        context['schedules'] = Schedule.objects.all()
    return render(request, 'core/index.html', context)

def booking(requset):
    pass

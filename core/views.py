from django.shortcuts import render
from .models import *


def index(request):
    context = {}
    context['schedules'] = Schedule.objects.all()

    return render(request, 'core/index.html', context)

from django.shortcuts import render, redirect,get_object_or_404
from django.db.models import Q
from .models import *
from .forms import BookingForm

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
        context['bookings'] = Booking.objects.filter(user = request.user)
    return render(request, 'core/index.html', context)

def booking(request, code):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        schedule = get_object_or_404(Schedule, code=code)
        if form.is_valid():
            print('Valid')
            book = form.save(commit=False)
            book.user = request.user
            book.schedule = schedule
            book.payment_status = True
            book.save()
            return redirect('detail', book.code)
        else:
            print(form.errors)
            return render(request, 'core/forms.html', {'form': form, 'code': code})
    else:
        return render(request, 'core/forms.html', {'form': BookingForm(), 'code': code})

def detail(request, code):
    booking = get_object_or_404(Booking, code=code)
    context = {'code': code, 'booking': booking}

    return render(request, 'core/details.html', context)

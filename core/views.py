from django.shortcuts import render, redirect,get_object_or_404
from django.db.models import Q
from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger,
)
from .models import *
from .forms import BookingForm

def index(request):
    return render(request, 'core/index.html')

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
            booked_seats = Booking.objects.filter(schedule=schedule).count()
            schedule.bus.number_of_seats = schedule.bus.number_of_seats - booked_seats
            schedule.bus.save()                
            return redirect('scheduled')
        else:
            print(form.errors)
            return render(request, 'core/forms.html', {'form': form, 'code': code})
    else:
        return render(request, 'core/forms.html', {'form': BookingForm(), 'code': code})

def scheduled(request):
    bookings = Booking.objects.filter(user=request.user)
    default_page = 1
    page = request.GET.get('page', default_page)
    items_per_page = 1
    paginator = Paginator(bookings, items_per_page)

    try:
        items_page = paginator.page(page)
    except PageNotAnInteger:
        items_page = paginator.page(default_page)
    except EmptyPage:
        items_page = paginator.page(paginator.num_pages)
    
    return render(request, 'core/scheduled_trip.html', {'bookings': items_page, 'items_page': items_page})

def delete_booking(request, code):
    booking = get_object_or_404(Booking, code=code)
    schedule = booking.schedule
    schedule.bus.number_of_seats += 1
    schedule.bus.save()
    booking.delete()

    return redirect('scheduled')

def find_trip(request):
    locations = Location.objects.all()
    context = {'locations': locations}
    return render(request, 'core/find-trip.html', context)

def searched_trip(request):
    depart = request.POST.get('depart')
    destination = request.POST.get('destination')
    schedules = Schedule.objects.filter(departure=depart, destination=destination)
    default_page = 1
    page = request.GET.get('page', default_page)
    items_per_page = 1
    paginator = Paginator(schedules, items_per_page)
    try:
        items_page = paginator.page(page)
    except PageNotAnInteger:
        items_page = paginator.page(default_page)
    except EmptyPage:
        items_page = paginator.page(paginator.num_pages)


    context = {
        'schedules': items_page, 
        'items_page': items_page,
        'depart': Location.objects.get(id=depart),
        'destination': Location.objects.get(id=destination)
        }
        
    return render(request, 'core/searched-trip.html', context)


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger,
)
from .models import *
from .forms import BookingForm
# from django.utils import timezone
from datetime import datetime


def index(request):
    return render(request, 'core/index.html')

@login_required
def booking(request, code):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        schedule = get_object_or_404(Schedule, code=code)
        
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user
            book.schedule = schedule
            book.save()
            booking_id = book.id
            
            request.session['pending_booking_id'] = booking_id
            request.session['pending_booking_price'] = schedule.price
    
            return redirect('payment_gateway:pay')

        else:
            # print(form.errors)
            return render(request, 'core/forms.html', {'form': form, 'code': code})
    else:
        schedule = get_object_or_404(Schedule, code=code)
        seat_taken = list(Booking.objects.filter(schedule=schedule).values_list('seat_number', flat=True))
        seats = schedule.bus.number_of_seats
        seat_available = [i for i in range(1, seats+1) if i not in seat_taken]

        return render(request, 'core/forms.html', {'form': BookingForm(), 'code': code, 'seat_available': seat_available})

@login_required
def scheduled(request):
    bookings = Booking.objects.filter(user=request.user, payment_status=True).order_by('-created')
    default_page = 1
    page = request.GET.get('page', default_page)
    items_per_page = 5
    paginator = Paginator(bookings, items_per_page)

    try:
        items_page = paginator.page(page)
    except PageNotAnInteger:
        items_page = paginator.page(default_page)
    except EmptyPage:
        items_page = paginator.page(paginator.num_pages)
    
    return render(request, 'core/scheduled_trip.html', {'bookings': items_page, 'items_page': items_page})

@login_required
def delete_booking(request, code):
    booking = get_object_or_404(Booking, code=code)
    schedule = booking.schedule
    schedule.bus.number_of_seats += 1
    schedule.bus.save()
    booking.delete()

    return redirect('core:scheduled')

def find_trip(request):
    locations = Location.objects.all()
    context = {'locations': locations}
    return render(request, 'core/find-trip.html', context)

def searched_trip(request):
    depart = request.POST.get('depart')
    destination = request.POST.get('destination')
    date_str = request.POST.get('date')
    date = datetime.strptime(date_str, '%Y-%m-%d').date()
    schedules = Schedule.objects.filter(departure=depart, destination=destination, date=date).order_by('-created')
    booked = [schedule for schedule in schedules if schedule.bookings.filter(user=request.user, payment_status=True).exists()]
  
    default_page = 1
    page = request.GET.get('page', default_page)
    items_per_page = 10
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
        'destination': Location.objects.get(id=destination),
        'date': request.POST.get('date'),
        'booked': booked,
        }
        
    return render(request, 'core/searched-trip.html', context)

# def update_schedule():
#     current_date = timezone.now().date()
#     schedule = Schedule.objects.filter(status='0')
#     completed_schedules = Schedule.objects.filter(date__lt=current_date, status='1')
#     cancelled_schedules = Schedule.objects.filter(status='0')
#     if cancelled_schedules.exists():
#         buses = Bus.objects.filter(schedule__in=cancelled_schedules)
#         for bus in buses:
#             initial_number_of_seats = bus._meta.get_field('number_of_seats').get_default()
#             bus.number_of_seats = initial_number_of_seats
#             bus.save()

#     for schedule in completed_schedules:
#         schedule_date = timezone.make_aware(schedule.date)

#         if schedule_date < current_date:
#             schedule.status = '2'
#             schedule.save()
#             bus = schedule.bus
#             initial_number_of_seats = bus._meta.get_field('number_of_seats').get_default()
#             bus.number_of_seats = initial_number_of_seats
#             bus.save()
from django.shortcuts import render, redirect,get_object_or_404
from django.db.models import Q
from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger,
)
from .models import *
from .forms import BookingForm
from django.utils import timezone




def update_schedule():
    current_date = timezone.now()
    completed_schedules = Schedule.objects.filter(date__lt=current_date, status='1')

    for schedule in completed_schedules:
        schedule.status = '2'
        schedule.save()

def index(request):
    update_schedule()
    return render(request, 'core/index.html')

def booking(request, code):
    update_schedule()
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
        schedule = get_object_or_404(Schedule, code=code)
        bookings = Booking.objects.filter(schedule=schedule)
        seat_taken = [booking.seat_number for booking in bookings]
        seat_available = []
        for i in range(51):
            if i in seat_taken:
                continue
            seat_available.append(i)
        return render(request, 'core/forms.html', {'form': BookingForm(), 'code': code, 'seat_available': seat_available})

def scheduled(request):
    update_schedule()
    bookings = Booking.objects.filter(user=request.user).order_by('-created')
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

def delete_booking(request, code):
    booking = get_object_or_404(Booking, code=code)
    schedule = booking.schedule
    schedule.bus.number_of_seats += 1
    schedule.bus.save()
    booking.delete()

    return redirect('scheduled')

def find_trip(request):
    update_schedule()
    locations = Location.objects.all()
    context = {'locations': locations}
    return render(request, 'core/find-trip.html', context)

def searched_trip(request):
    update_schedule()
    depart = request.POST.get('depart')
    destination = request.POST.get('destination')
    schedules = Schedule.objects.filter(departure=depart, destination=destination).order_by('-created')
    booked = []
    for schedule in schedules:
        for b in schedule.bookings.all():
            if b.user == request.user:
               booked.append(schedule)
    
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

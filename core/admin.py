from django.contrib import admin
from .models import User, Booking, Bus, Schedule, Location

admin.site.register(User)
admin.site.register(Booking)
admin.site.register(Bus)
admin.site.register(Schedule)
admin.site.register(Location)

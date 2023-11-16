from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import uuid

class User(AbstractUser):
    name = models.CharField(max_length=100, unique=True)
    phone_number = PhoneNumberField(blank=True)
    email = models.EmailField(unique=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_number']

    def __str__(self):
        return f"{self.name or self.username} ({self.phone_number})"

class Bus(models.Model):
    name = models.CharField(max_length=100)
    number = models.PositiveIntegerField()
    status = models.BooleanField(default=True)
    driver = models.CharField(max_length=100)
    number_of_seats = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.name} ({self.number}/{self.number_of_seats} seats)"

class Location(models.Model):
    name = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name}"

class Schedule(models.Model):
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    departure = models.ForeignKey(Location, related_name='departures', on_delete=models.CASCADE)
    destination = models.ForeignKey(Location, related_name='destinations', on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.departure} to {self.destination} (Bus: {self.bus.name}/{self.bus.number})"

class Booking(models.Model):
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user.name} - {self.schedule.__Str__()}"
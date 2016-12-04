from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# from .models import Patient, Record, Professional

  
class Professional(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    dni = models.IntegerField()
    phone_number = models.CharField(max_length=15)
    profession = models.CharField(max_length=100)
    def __str__(self):
        return str(self.dni)

class Patient(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birthdate = models.DateField()
    health_insurance = models.CharField(max_length=100)
    dni = models.IntegerField()

    def __str__(self):
        return (self.first_name + " " + self.last_name)

class Record(models.Model):
    creation_datetime = models.DateTimeField(auto_now_add=True)
    session_datetime = models.DateTimeField()
    session_resume = models.CharField(max_length=1000)
    professional = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # change to professional when user has been extended
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True)
    session_duration = models.DurationField()

    def __str__(self):
        return (self.professional.get_full_name() + " - " + 
                self.patient.__str__() + " - Fecha de la sesion: " + str(self.session_datetime.date()))


# Create your models here.

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Professional(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    dni = models.IntegerField(default='0')
    phone_number = models.CharField(max_length=15, default='0')
    profession = models.CharField(max_length=100, default='')
    def __str__(self):
        return str(self.dni)


#@receiver(post_save, sender=User)
#def create_user_profile(sender, instance, created, **kwargs):
#    if created:
#        Professional.objects.create(user=instance)

#@receiver(post_save, sender=User)
#def save_user_profile(sender, instance, **kwargs):
#    instance.professional.save()

class Patient(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birthdate = models.DateField()
    health_insurance = models.CharField(max_length=100)
    dni = models.IntegerField()
    phone_number = models.CharField(max_length=30, null=True)

    def get_full_name(self):
        return (self.first_name + " " + self.last_name)

    def __str__(self):
        return self.get_full_name()

    def get_age(self):
        return ((timezone.now().date()) - self.birthdate)


class Case(models.Model):
    professional = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True)
    coordinator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class Record(models.Model):
    creation_datetime = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    session_datetime = models.DateTimeField()
    session_resume = models.CharField(max_length=1000)
    session_duration = models.IntegerField()
    case = models.ForeignKey(Case, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return (self.case.professional.get_full_name() + " - " + 
                self.case.patient.__str__() + " - Fecha de la sesion: " +
                str(self.session_datetime.date()))




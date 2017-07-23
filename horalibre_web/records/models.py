# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Professional(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    dni = models.IntegerField()
    phone_number = models.CharField(max_length=15)
    profession = models.CharField(max_length=100)
    is_coordinator = models.BooleanField(default=False)

    def get_full_name(self):
        return (self.user.first_name + " " + self.user.last_name)

    def __str__(self):
        return str(self.user.last_name + ", " + self.user.first_name + ' (DNI:' + str(self.dni) + ')')


class Secretary(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    dni = models.IntegerField()
    phone_number = models.CharField(max_length=15)
    
    def get_full_name(self):
        return (self.user.first_name + " " + self.user.last_name)

    def __str__(self):
        return str(self.user.last_name + ", " + self.user.first_name +
                  ' (DNI:' + str(self.dni) + ')')


class Patient(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birthdate = models.DateField()
    health_insurance = models.CharField(max_length=100)
    dni = models.IntegerField()
    phone_number = models.CharField(max_length=30, null=True)

    def get_full_name(self):
        return (self.first_name + " " + self.last_name)

    def get_age(self):
        return ((timezone.now().date()) - self.birthdate)

    def __str__(self):
        return str(self.last_name + ", " + self.first_name +
                   ' (DNI:' + str(self.dni) + ')')


# CHANGE ON_DELETE to default user
class Case(models.Model):
    professional = models.ForeignKey(Professional, related_name='case_prof', 
                   on_delete=models.SET_NULL, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True)
    coordinator = models.ForeignKey(Professional, related_name='case_coord',
                  on_delete=models.SET_NULL, null=True)

    def __str__(self):
        prof_name = patient_name = coord_name = ""
        if self.professional is None:
            prof_name = "Profesional eliminado"
        else:
            prof_name = self.professional.get_full_name()
        
        if self.patient is None:
            patient_name = "Paciente eliminado"
        else:
            patient_name = self.patient.get_full_name()
        
        if self.coordinator is None:
            coord_name = "Coordinador eliminado"
        else:
            coord_name = self.coordinator.get_full_name()

        return ("Paciente: \"" + patient_name + "\" ~ Profesional: \"" + prof_name + "\" ~ Coordinador: \"" + coord_name + "\"")
    
    def log_str(self):
        prof_name = patient_name = coord_name = ""
        if self.professional is None:
            prof_name = "Profesional eliminado"
        else:
            prof_name = self.professional.get_full_name()

        if self.patient is None:
            patient_name = "Paciente eliminado"
        else:
            patient_name = self.patient.get_full_name()
        
        if self.coordinator is None:
            coord_name = "Coordinador eliminado"
        else:
            coord_name = self.coordinator.get_full_name()

        return str(patient_name + " - " + prof_name + " - " + coord_name + " (id: " + str(self.id) + ")")


class Record(models.Model):
    creation_datetime = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    session_datetime = models.DateTimeField()
    session_resume = models.CharField(max_length=5000)
    session_duration = models.IntegerField()
    author = models.ForeignKey(Professional, related_name='record_author', 
                   on_delete=models.SET_NULL, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL,
                                null=True, related_name='record_patient')
    case = models.ForeignKey(Case, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        if self.author:
            author = self.author.get_full_name()
        else:
            author = "Profesional Eliminado"

        if self.case is None:
            return "Deleted Case, resume:" + self.session_resume[:40] + "..."
        else:
            return (author + " - " + 
                    self.case.patient.__str__() + " - Fecha de la sesion: " +
                    str(self.session_datetime.date()))

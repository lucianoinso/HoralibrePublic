# -*- coding: utf-8 -*-
from django.db import models
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from datetime import datetime

# Project imports
from records.models import Professional, Secretary, Patient, Record, Case

"""class NameForm(forms.Form):
    your_name = forms.CharField(widget=forms.TextInput(
                                attrs={
                                    'class': 'administration-input',
                                })
                                ,label='Your Name', max_length = 40)
    sender = forms.EmailField()
    message = forms.CharField(error_messages={'required': 'Pol favol tipea un correo correto joer'},
                              widget=forms.Textarea(
                              attrs={
                                    'class': 'edit-record-textarea',
                                }),
                              )
    cc_myself = forms.BooleanField(required=False)
    date = forms.widget=forms.SelectDateWidget() """

class ProfessionalListForm(forms.Form):
    professional = forms.ModelChoiceField(queryset=Professional.objects.all().order_by('user__last_name'))


class ProfessionalForm(ModelForm):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    username = forms.CharField(max_length = 150, label='Nombre de usuario')
    password = forms.CharField(widget=forms.PasswordInput, max_length = 50,
                               label='Contraseña')
    first_name = forms.CharField(max_length = 30, label='Nombre')
    last_name = forms.CharField(max_length = 30, label='Apellido')
    email = forms.EmailField()
    class Meta:
        model = Professional
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 
                  'dni', 'phone_number', 'profession', 'is_coordinator',
                 ]
        labels = {
            "dni": "Número de documento",
            "phone_number": "Número de teléfono",
            "profession": "Profesión",
            "is_coordinator": "Es coordinador?",
        }
        widgets = {}


class SecretaryForm(ModelForm):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    username = forms.CharField(max_length = 150, label='Nombre de usuario')
    password = forms.CharField(widget=forms.PasswordInput, max_length = 50,
                               label='Contraseña')
    first_name = forms.CharField(max_length = 30, label='Nombre')
    last_name = forms.CharField(max_length = 30, label='Apellido')
    email = forms.EmailField()
    class Meta:
        model = Secretary
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 
                  'dni', 'phone_number',
                 ]
        labels = {
            "dni": "Número de documento",
            "phone_number": "Número de teléfono",
        }

class SecretaryListForm(forms.Form):
    secretary = forms.ModelChoiceField(queryset=Secretary.objects.all().order_by('user__last_name'))


class PatientForm(ModelForm):
    birthdate_year_choices = set((year) for year in range(datetime.now().year - 110, datetime.now().year + 1))
    birthdate = forms.DateField(widget=forms.SelectDateWidget(years=birthdate_year_choices),
                                label='Fecha de nacimiento')
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'birthdate', 'health_insurance', 'dni', 
                  'phone_number']
        labels = {
            "first_name": "Nombre",
            "last_name": "Apellido",
            "birthdate": "Fecha de nacimiento",
            "health_insurance": "Obra Social",
            'dni': "D.N.I",
            "phone_number": "Numero de teléfono",
        }
        error_messages = {
            'dni': {
                'max_value': "El numero ingresado es demasiado largo.",
                'invalid': "El numero ingresado es invalido.",
            },
        }

class PatientListForm(forms.Form):
    patient = forms.ModelChoiceField(queryset=Patient.objects.all().order_by('last_name'))


class CaseForm(ModelForm):
    coordinator = forms.ModelChoiceField(queryset=Professional.objects.filter(is_coordinator=True).order_by('user__last_name'))
    class Meta:
        model = Case
        fields = ['patient','professional','coordinator']

class CaseListForm(forms.Form):
    case = forms.ModelChoiceField(queryset=Case.objects.all().order_by('coordinator__user__last_name'))
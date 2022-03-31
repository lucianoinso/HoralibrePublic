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
    username = forms.CharField(max_length = 150, label='Nombre de usuario',
                               widget=forms.TextInput(attrs={'autocomplete':'off'}))
    password = forms.CharField(widget=forms.PasswordInput, max_length = 50,
                               label='Contraseña')
    first_name = forms.CharField(max_length = 30, label='Nombre',
                                 widget=forms.TextInput(attrs={'autocomplete':'off'}))
    last_name = forms.CharField(max_length = 30, label='Apellido',
                                widget=forms.TextInput(attrs={'autocomplete':'off'}))
    email = forms.EmailField(error_messages={'invalid':"Ingrese un correo electronico valido."},
                             widget=forms.TextInput(attrs={'autocomplete':'off'}))
    is_staff = forms.BooleanField(initial=False, required=False, label='Es administradór')
    is_active = forms.BooleanField(initial=True, required=False, label='Cuenta activa')

    class Meta:
        model = Professional
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 
                  'dni', 'phone_number', 'profession', 'is_coordinator', 'is_staff',
                  'is_active',
                 ]
        labels = {
            "dni": "Número de documento",
            "phone_number": "Número de teléfono",
            "profession": "Profesión",
            "is_coordinator": "Es coordinador",
        }
        error_messages = {
            'dni': {
                'max_value': "El numero ingresado es demasiado largo.",
                'invalid': "El numero ingresado es invalido.",
            },
        }
        widgets = {
            "phone_number":forms.TextInput(attrs={'autocomplete':'off'})
        }

class ChangePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, max_length = 50,
                               label='Contraseña nueva')

class ProfessionalEditForm(ModelForm):
    username = forms.CharField(max_length = 150, label='Nombre de usuario',
                               widget=forms.TextInput(attrs={'autocomplete':'off'}))
    first_name = forms.CharField(max_length = 30, label='Nombre',
                                 widget=forms.TextInput(attrs={'autocomplete':'off'}))
    last_name = forms.CharField(max_length = 30, label='Apellido',
                                 widget=forms.TextInput(attrs={'autocomplete':'off'}))
    email = forms.EmailField(error_messages={'invalid':"Ingrese un correo electronico valido."},
                             widget=forms.TextInput(attrs={'autocomplete':'off'}))
    is_staff = forms.BooleanField(required=False, label='Es administradór')
    is_active = forms.BooleanField(initial=True, required=False, label='Cuenta activa')
    class Meta:
        model = Professional
        fields = ['username', 'first_name', 'last_name', 'email',
                  'dni', 'phone_number', 'profession', 'is_coordinator',
                  'is_staff', 'is_active',
                 ]
        labels = {
            "dni": "Número de documento",
            "phone_number": "Número de teléfono",
            "profession": "Profesión",
            "is_coordinator": "Es coordinador",
        }
        error_messages = {
            'dni': {
                'max_value': "El numero ingresado es demasiado largo.",
                'invalid': "El numero ingresado es invalido.",
            },
        }
        widgets = {
            "phone_number":forms.TextInput(attrs={'autocomplete':'off'})
        }

class SecretaryForm(ModelForm):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    username = forms.CharField(max_length = 150, label='Nombre de usuario',
                               widget=forms.TextInput(attrs={'autocomplete':'off'}))
    password = forms.CharField(widget=forms.PasswordInput, max_length = 50,
                               label='Contraseña')
    first_name = forms.CharField(max_length = 30, label='Nombre',
                               widget=forms.TextInput(attrs={'autocomplete':'off'}))
    last_name = forms.CharField(max_length = 30, label='Apellido',
                               widget=forms.TextInput(attrs={'autocomplete':'off'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'autocomplete':'off'}))
    is_active = forms.BooleanField(initial=True, required=False, label='Cuenta activa')
    class Meta:
        model = Secretary
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 
                  'dni', 'phone_number', 'is_active',
                 ]
        labels = {
            "dni": "Número de documento",
            "phone_number": "Número de teléfono",
        }
        error_messages = {
            'dni': {
                'max_value': "El numero ingresado es demasiado largo.",
                'invalid': "El numero ingresado es invalido.",
            },
        }
        widgets = {
            "phone_number":forms.TextInput(attrs={'autocomplete':'off'})
        }

class SecretaryEditForm(ModelForm):
    username = forms.CharField(max_length = 150, label='Nombre de usuario',
                               widget=forms.TextInput(attrs={'autocomplete':'off'}))
    first_name = forms.CharField(max_length = 30, label='Nombre',
                               widget=forms.TextInput(attrs={'autocomplete':'off'}))
    last_name = forms.CharField(max_length = 30, label='Apellido',
                               widget=forms.TextInput(attrs={'autocomplete':'off'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'autocomplete':'off'}))
    is_active = forms.BooleanField(initial=True, required=False, label='Cuenta activa')
    class Meta:
        model = Secretary
        fields = ['username', 'first_name', 'last_name', 'email', 
                  'dni', 'phone_number', 'is_active',
                 ]
        labels = {
            "dni": "Número de documento",
            "phone_number": "Número de teléfono",
        }
        error_messages = {
            'dni': {
                'max_value': "El numero ingresado es demasiado largo.",
                'invalid': "El numero ingresado es invalido.",
            },
        }
        widgets = {
            "phone_number":forms.TextInput(attrs={'autocomplete':'off'})
        }

class SecretaryListForm(forms.Form):
    secretary = forms.ModelChoiceField(queryset=Secretary.objects.all().order_by('user__last_name')
                                       ,label='Secretarias')

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
        widgets = {
            "first_name":forms.TextInput(attrs={'autocomplete':'off'}),
            "last_name":forms.TextInput(attrs={'autocomplete':'off'}),
            "phone_number":forms.TextInput(attrs={'autocomplete':'off'}),
        }


class PatientListForm(forms.Form):
    patient = forms.ModelChoiceField(queryset=Patient.objects.all().order_by('last_name'))


class CaseForm(ModelForm):
    coordinator = forms.ModelChoiceField(queryset=Professional.objects.filter(is_coordinator=True).order_by('user__last_name'),
                                         label='Coordinador')
    class Meta:
        model = Case
        fields = ['patient','professional','coordinator']
        labels = {
            'patient': "Paciente",
            'professional': "Profesional",
        }

class CaseListForm(forms.Form):
    case = forms.ModelChoiceField(queryset=Case.objects.all().order_by('patient__last_name'))
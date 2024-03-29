# -*- coding: utf-8 -*-

# Python Imports
from datetime import datetime

# Django Imports
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

# Project Imports
from login.views import redirect_home
from .models import Patient, Record, Professional, Case, Notification
from commentary.models import Comment


def select_records(request, patient_id):
    if request.user.is_authenticated:
        patient = Patient.objects.get(id=patient_id)
        return render(request, 'records/select_records.html', {
            'patient': patient,
            })
    else:
        return HttpResponseRedirect("/login")


def patient_list(request):
    if request.user.is_authenticated:
        try:
            prof = Professional.objects.get(user=request.user)
            cases = Case.objects.all().filter(Q(professional=prof) | Q(coordinator=prof))\
                                .distinct('patient').values_list('id', flat=True)
            case_list = Case.objects.filter(id__in=cases).order_by('patient__last_name')

        except Exception as e:
            return redirect_home()

        return render(request, 'records/patient_list.html', {
            'case_list': case_list,
            })
    else:
        return HttpResponseRedirect("/login")


def my_records_list(request, patient_id):
    if request.user.is_authenticated:
        try:
            professional = Professional.objects.get(user=request.user)
            patient = Patient.objects.get(id=patient_id)
            case = Case.objects.filter(Q(patient=patient),
                                       Q(professional=professional) | Q(coordinator=professional))
            if not case:
                raise ObjectDoesNotExist

            record_list = Record.objects.all().filter(author=professional,patient=patient).order_by('-session_datetime')
            paginator = Paginator(record_list, 15) # Show 15 records per page
            page = request.GET.get('page')
            page_records = paginator.page(page)

        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            page_records = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            page_records = paginator.page(paginator.num_pages)

        except ObjectDoesNotExist:
            return redirect_home()

        except Exception as e:
            print(e)
            return redirect_home()

        return render(request, 'records/record_list.html', {
            'page_records': page_records,
            'patient': patient,
            })
    else:
        return HttpResponseRedirect("/login")


def all_records_list(request, patient_id):
    if request.user.is_authenticated:
        try:
            prof = Professional.objects.get(user=request.user)
            patient = Patient.objects.get(id=patient_id)
            # Check if the logged user is inside any of the cases of the patient
            case = Case.objects.filter(Q(patient=patient), Q(professional=prof) | Q(coordinator=prof))

            if not case:
                # If it's not in any of the cases (it's trying to access a
                # record from a patient he doesn't have), redirect to homepage
                raise ObjectDoesNotExist

            record_list = Record.objects.all().filter(patient=patient).order_by('-session_datetime')

            paginator = Paginator(record_list, 15) # Show 15 records per page
            page = request.GET.get('page')
            page_records = paginator.page(page)

        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            page_records = paginator.page(1)

        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            page_records = paginator.page(paginator.num_pages)

        except ObjectDoesNotExist:
            return redirect_home()

        except Exception as e:
            print(e)
            return redirect_home()

        return render(request, 'records/record_list.html', {
            'page_records': page_records,
            'patient': patient,
            })
    else:
        return HttpResponseRedirect("/login")

"""
def send_notifications():
    try:
        notifs = Notification.objects.all()
        coords = set()
        email_list = []
        for notif in notifs:
            coords.add(notif.record.case.coordinator.user.email)

        coords_content = dict.fromkeys(coords, "")

        for notif in notifs:
            notif_content = ("<li style=\"margin-bottom:5px;\">" + (notif.record.author.get_full_name()) + " ha agregado un registro nuevo para el/la paciente " +
                            (notif.record.patient).get_full_name() + " " + "<a href=\"" + "http://fundacionhoralibre-sitetest.rhcloud.com/home/records/patient/"+ str(notif.record.patient.id) + "/record/" + str(notif.record.id) + "/" + "\">" + "(" + (notif.record.session_datetime).strftime('%d/%m/%Y') + ")</a>.</li>")
            coords_content[notif.record.case.coordinator.user.email] += notif_content

        for coord in coords_content:
            html_message = u"<!DOCTYPE HTML><html><body><h3>Estimado/a, le acercamos las últimas novedades de registros vinculadas a sus casos:</h3><ul style=\"padding-left:10px;\">" + coords_content[coord] + u"</ul><p style=\"padding-top:10px\">Atte.<br>El equipo de Fundación Hora Libre</p></body></html>"
            # send_mail('SUBJECT','CONTENT','from@email.com',['dest1@hotmail.com', 'dest2@hotmail.com'],fail_silently=False)
            send_mail('Novedades de registros', "",
                      settings.EMAIL_HOST_USER, [coord], fail_silently=False,
                      html_message=html_message)

        return HttpResponse("Notifications sent")

    except Exception as e:
        print (e)
"""

def record_detail(request, patient_id, record_id):
    try:
        if request.user.is_authenticated:
            prof = Professional.objects.get(user=request.user)
            patient = Patient.objects.get(id=patient_id)
            case = Case.objects.all().filter(Q(professional=prof) | Q(coordinator=prof)
                                            ,Q(patient=patient))
            if case:
                try:
                    record = Record.objects.get(id=record_id)
                    comments = (Comment.objects.all().filter(record=record)
                                   .order_by('create_date'))
                    # Assuming there is only one coordinator per patient, if the 
                    # record is case-orphan we assign the new case to the first case 
                    # that has professional as a professional or as a coordinator, 
                    # and patient as a patient
                    if record.case is None:
                        record.case = case.first()
                        record.save()

                except ObjectDoesNotExist:
                    return redirect_home()

                except Exception as e:
                    return HttpResponse(e)

                return render(request, 'records/record_detail.html', {
                    'record': record,
                    'comments': comments,
                    })
            else:
                return redirect_home()
        else:
            return HttpResponseRedirect("/login")
    except Exception as e:
        print e
        return redirect_home()


def create_record_from_patient(request, patient_id):
    try:
        if request.user.is_authenticated:
            professional = Professional.objects.get(user=request.user)
            patient = Patient.objects.get(id=patient_id)
            case = Case.objects.all().filter(Q(patient=patient),
                                             Q(professional=professional) | Q(coordinator=professional))
            if case:
                if request.method == "POST":
                    ses_dur_hrs = request.POST.get("session_duration_hours")
                    ses_dur_mins = request.POST.get("session_duration_minutes")
                    session_duration = datetime.strptime(ses_dur_hrs + ":" + ses_dur_mins, '%H:%M')
                    record = Record(session_datetime=request.POST.get("session_datetime"),
                                    session_resume=request.POST.get("session_resume"),
                                    case=case.first(), author=professional,
                                    patient=patient,
                                    session_duration=session_duration)
                    record.save()
                    notification = Notification(record=record)
                    notification.save()
                    return redirect_my_patient_records(patient_id)
                else:
                    return render(request, 'records/create_record_from_patient.html', {'patient': patient })
            else:
                return redirect_home()
        else:
            return HttpResponseRedirect("/login")
    except Exception as e:
        print e
        return HttpResponseRedirect("/login")


def edit_record(request, patient_id, record_id):
    try:
        if request.user.is_authenticated:
            record = get_object_or_404(Record, id=record_id)
            if request.user == record.author.user:
                if request.method == "POST":
                    if request.POST.get("session_datetime"):
                        record.session_datetime = request.POST.get("session_datetime")
                    if (request.POST.get("session_duration_hours") and
                        request.POST.get("session_duration_minutes")):
                        ses_dur_hrs = request.POST.get("session_duration_hours")
                        ses_dur_mins = request.POST.get("session_duration_minutes")
                        session_duration = datetime.strptime(ses_dur_hrs + ":" + ses_dur_mins, '%H:%M')
                        record.session_duration = session_duration
                    if request.POST.get("session_resume"):
                        record.session_resume = request.POST.get("session_resume")
                    record.save()
                    return redirect_record(patient_id, record_id)
                else:
                    ses_dur_hrs = record.session_duration.strftime('%H')
                    ses_dur_mins = record.session_duration.strftime('%M')
                    return render(request, 'records/edit_record.html',
                                  {'record': record,
                                   'session_duration_hours': ses_dur_hrs,
                                   'session_duration_minutes': ses_dur_mins,
                                  }
                                 )
            else:
                return redirect_home()
        else:
            return HttpResponseRedirect("/login")
    except Exception as e:
        print e
        return redirect_home()


def delete_record(request, patient_id, record_id):
    if request.user.is_authenticated:
        record = get_object_or_404(Record, id=record_id)
        if record.author.user == request.user:
            record.delete()
            return redirect_my_patient_records(patient_id)
        else:
            return redirect_home()
    else:
        return HttpResponseRedirect("/login")


def redirect_patient_list():
    return HttpResponseRedirect("/home/records/patient_list")


def redirect_record(patient_id, record_id):
    return HttpResponseRedirect("/home/records/patient/{}/record/{}".
                                format(patient_id, record_id))

def redirect_my_patient_records(patient_id):
    return HttpResponseRedirect("/home/records/patient/{}/my_records".format(patient_id))

def redirect_all_patient_records(patient_id):
    return HttpResponseRedirect("/home/records/{}".format(patient_id))
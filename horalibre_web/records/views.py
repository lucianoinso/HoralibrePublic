# Django Imports
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Project Imports
from login.views import redirect_home
from .models import Patient, Record, Professional, Case
from commentary.models import Comment


def select_records(request, username, patient_id):
    if request.user.is_authenticated:
        if request.user.username == username:
            patient = Patient.objects.get(pk=patient_id)
            return render(request, 'records/select_records.html', {
                'username': username,
                'patient': patient,
                })
        else:
            return redirect_home(request.user.username)
    else:
        return HttpResponseRedirect("/login")


def patient_list(request, username="Anonymous"):
    if request.user.is_authenticated:
        if request.user.username == username:
            try:
                user = User.objects.get(username=username)
                case_list = Case.objects.all().filter(professional=user)
#                record_list = Record.objects.filter(professional=user).distinct('patient')
            except Exception as e:
                return HttpResponse(e)

            return render(request, 'records/patient_list.html', {
                'case_list': case_list,
                'username': username,
                })
        else:
            return redirect_home(request.user.username)
    else:
        return HttpResponseRedirect("/login")


def my_records_list(request, username, patient_id):
    if request.user.is_authenticated:
        if request.user.username == username:
                try:
                    user = User.objects.get(username=username)
                    patient = Patient.objects.get(pk=patient_id)
                    case = Case.objects.filter(professional=user).filter(patient=patient)
                    record_list = (Record.objects.all().filter(case=case).order_by('-session_datetime'))
                    paginator = Paginator(record_list, 15) # Show 15 records per page
                    page = request.GET.get('page')
                    page_records = paginator.page(page)

                except PageNotAnInteger:
                    # If page is not an integer, deliver first page.
                    page_records = paginator.page(1)
                except EmptyPage:
                    # If page is out of range (e.g. 9999), deliver last page of results.
                    page_records = paginator.page(paginator.num_pages)

                except Exception as e:
                    return HttpResponse(e)

                return render(request, 'records/record_list.html', {
                    'page_records': page_records,
                    'username': username,
                    'patient': patient,
                    'case': case,
                    })
        else:
            return redirect_home(request.user.username)
    else:
        return HttpResponseRedirect("/login")


def all_records_list(request, username, patient_id):
    if request.user.is_authenticated:
        if request.user.username == username:
            try:
                user = User.objects.get(username=username)
                patient = Patient.objects.get(pk=patient_id)
                case = Case.objects.filter(patient=patient)
                record_list = (Record.objects.all().filter(case_id__in=case).order_by('-session_datetime'))

                paginator = Paginator(record_list, 15) # Show 15 records per page
                page = request.GET.get('page')
                page_records = paginator.page(page)

            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                page_records = paginator.page(1)

            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                page_records = paginator.page(paginator.num_pages)

            except Exception as e:
                return HttpResponse(e)

            return render(request, 'records/record_list.html', {
                'page_records': page_records,
                'username': username,
                'patient': patient,
                'case': case,
                })
        else:
            return redirect_home(request.user.username)
    else:
        return HttpResponseRedirect("/login")


def record_detail(request, username, patient_id, record_id):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        patient = Patient.objects.get(pk=patient_id)
        case = Case.objects.all().filter(professional=user, patient=patient)

        if case:
            try:
                record = Record.objects.get(pk=record_id)
                comments = (Comment.objects.all().filter(record=record)
                               .order_by('create_date'))
            except Exception as e:
                return HttpResponse(e)

            return render(request, 'records/record_detail.html', {
                'record': record,
                'comments': comments,
                })
        else:
            return redirect_home(request.user.username)
    else:
        return HttpResponseRedirect("/login")


def create_record_from_patient(request, username, patient_id):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        if request.user == user:
            patient = Patient.objects.get(pk=patient_id)
            if request.method == "POST":
                case = Case.objects.get(professional=user, patient=patient)
                record = Record(session_datetime=request.POST.get("session_datetime"),
                                session_resume=request.POST.get("session_resume"),
                                case=case,
                                session_duration = request.POST.get("session_duration"))
                record.save()
                # check why username is the id, request.user.username is the user
                return redirect_my_patient_records(request.user.username, patient_id)
            else:
                return render(request, 'records/create_record_from_patient.html', {'user': user, 'patient': patient })
    else:
        return HttpResponseRedirect("/login")


def create_record(request, username):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        case_list = Case.objects.all().filter(professional=user)

        if request.user == user:
            if request.method == "POST":
                patient = Patient.objects.get(pk=request.POST.get("patient_from_list"))
                case = Case.objects.get(professional=user, patient=patient)
                record = Record(session_datetime=request.POST.get("session_datetime"),
                                session_resume=request.POST.get("session_resume"),
                                case=case,
                                session_duration = request.POST.get("session_duration"))
                record.save()
                return redirect_patient_list(request.user.username)
            else:
                return render(request, 'records/create_record.html', {'user': user, 'case_list': case_list })
        else:
            return redirect_my_patient_records(request.user.username, patient_id)
    else:
        return HttpResponseRedirect("/login")


def edit_record(request, username, patient_id, record_id):
    if request.user.is_authenticated:
        record = get_object_or_404(Record, pk=record_id)
        if request.user == record.case.professional:
            if request.method == "POST":
                if request.POST.get("session_datetime"):
                    record.session_datetime = request.POST.get("session_datetime")
                if request.POST.get("session_duration"):
                    record.session_duration = request.POST.get("session_duration")
                if request.POST.get("session_resume"):
                    record.session_resume = request.POST.get("session_resume")
                record.save()
                return redirect_record(username, patient_id, record_id)
            else:
                return render(request, 'records/edit_record.html', {'record': record})
        else:
            return redirect_home(request.user.username)
    else:
        return HttpResponseRedirect("/login")


def delete_record(request, username, patient_id, record_id):
    if request.user.is_authenticated:
        record = get_object_or_404(Record, pk=record_id)
        if request.user == record.case.professional:
            record.delete()
            return redirect_my_patient_records(request.user.username, patient_id)
        else:
            return redirect_home(request.user.username)
    else:
        return HttpResponseRedirect("/login")


"""
def patient_list(request, username):
    if request.user.is_authenticated:
        
        goal = get_object_or_404(Goal, pk=goal_id)
        if request.user == goal.owner:
            comments = (Comment.objects.all().filter(goal=goal)
                               .order_by('-create_date'))
            return render(request, 'goal/detail.html',
                          {'goal': goal, 'comments': comments})
    return redirect_home(request.user)


def new_record(request):
    if request.user.is_authenticated:
        try:
            user = User.objects.get(username=request.user.username)
        except Exception as e:
            return HttpResponse("El usuario no existe")
        if request.method == "POST":
            finish_date = request.POST.get("finish_date")
            if finish_date == '':
                finish_date = timezone.now()
            record = record.objects.create(record_text=request.POST.get("record_text"),
                                       finish_date=finish_date,
                                       create_date=timezone.now(),
                                       priority=request.POST.get("priority"),
                                       state=request.POST.get("state"),
                                       owner=user
                                       )
            record.save()
            return redirect_home(request.user.username)
        else:
            return render(request, 'record/new_record.html')
    else:
        return HttpResponseRedirect("/login")


def detail_record(request, record_id):
    if request.user.is_authenticated:
        record = get_object_or_404(record, pk=record_id)
        if request.user == record.owner:
            comments = (Comment.objects.all().filter(record=record)
                               .order_by('-create_date'))
            return render(request, 'record/detail.html',
                          {'record': record, 'comments': comments})
    return redirect_home(request.user)
"""

def redirect_patient_list(username):
    return HttpResponseRedirect("/home/{}/records/patient_list".format(username))


def redirect_record(username, patient_id, record_id):
    return HttpResponseRedirect("/home/{}/records/patient/{}/record/{}".
                                format(username, patient_id, record_id))

def redirect_my_patient_records(username, patient_id):
    return HttpResponseRedirect("/home/{}/records/patient/{}/my_records".format(username, patient_id))

def redirect_all_patient_records(username, patient_id):
    return HttpResponseRedirect("/home/{}/records/{}".format(username, patient_id))
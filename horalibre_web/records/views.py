# Django Imports
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

# Project Imports
from login.views import redirect_home
from .models import Patient, Record, Professional, Case
from commentary.models import Comment


def select_records(request, patient_id):
    if request.user.is_authenticated:
        patient = Patient.objects.get(id=patient_id)
        return render(request, 'records/select_records.html', {
            'patient': patient,
            })
    else:
        return HttpResponseRedirect("/login")

# CHECK THIS SHIT
def patient_list(request):
    if request.user.is_authenticated:
        try:
            prof = Professional.objects.get(user__username=request.user.username)
            case_list = Case.objects.all().filter(Q(professional=prof) | Q(coordinator=prof))
#                record_list = Record.objects.filter(professional=user).distinct('patient')
            print case_list
        except Exception as e:
            print "lcdtm"
            return HttpResponse(e)

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
#            case = Case.objects.filter(professional=professional).filter(patient=patient)
            record_list = Record.objects.all().filter(author=professional,case__patient=patient).order_by('-session_datetime')
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
            'patient': patient,
#            'case': case,
            })
    else:
        return HttpResponseRedirect("/login")

# CHECK PERMISSIONS
def all_records_list(request, patient_id):
    if request.user.is_authenticated:
        try:
            patient = Patient.objects.get(id=patient_id)
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
            'patient': patient,
            'case': case,
            })
    else:
        return HttpResponseRedirect("/login")


def record_detail(request, patient_id, record_id):
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


def create_record_from_patient(request, patient_id):
    if request.user.is_authenticated:
        professional = Professional.objects.get(user=request.user)
        patient = Patient.objects.get(id=patient_id)
        if request.method == "POST":
            case = Case.objects.filter(Q(patient=patient),
                                       Q(professional=professional) | Q(coordinator=professional)).first()
            print case
            record = Record(session_datetime=request.POST.get("session_datetime"),
                            session_resume=request.POST.get("session_resume"),
                            case=case, author=professional,
                            session_duration=request.POST.get("session_duration"))
            record.save()
            # check why username is the id, request.user.username is the user
            return redirect_my_patient_records(patient_id)
        else:
            return render(request, 'records/create_record_from_patient.html', {'patient': patient })
    else:
        return HttpResponseRedirect("/login")

"""
def create_record(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        case_list = Case.objects.all().filter(professional=user)

        if request.user == user:
            if request.method == "POST":
                patient = Patient.objects.get(id=request.POST.get("patient_from_list"))
                case = Case.objects.get(professional=user, patient=patient)
                record = Record(session_datetime=request.POST.get("session_datetime"),
                                session_resume=request.POST.get("session_resume"),
                                case=case,

                                session_duration = request.POST.get("session_duration"))
                record.save()
                return redirect_patient_list()
            else:
                return render(request, 'records/create_record.html', {'user': user, 'case_list': case_list })
        else:
            return redirect_my_patient_records(request.user.username, patient_id)
    else:
        return HttpResponseRedirect("/login")
"""


def edit_record(request, patient_id, record_id):
    if request.user.is_authenticated:
        record = get_object_or_404(Record, id=record_id)
        if request.user == record.author.user:
            if request.method == "POST":
                if request.POST.get("session_datetime"):
                    record.session_datetime = request.POST.get("session_datetime")
                if request.POST.get("session_duration"):
                    record.session_duration = request.POST.get("session_duration")
                if request.POST.get("session_resume"):
                    record.session_resume = request.POST.get("session_resume")
                record.save()
                return redirect_record(patient_id, record_id)
            else:
                return render(request, 'records/edit_record.html', {'record': record})
        else:
            return redirect_home(request.user.username)
    else:
        return HttpResponseRedirect("/login")


def delete_record(request, patient_id, record_id):
    if request.user.is_authenticated:
        record = get_object_or_404(Record, id=record_id)
        if record.author.user == request.user:
            record.delete()
            return redirect_my_patient_records(patient_id)
        else:
            return redirect_home(request.user.username)
    else:
        return HttpResponseRedirect("/login")


"""
def patient_list(request, username):
    if request.user.is_authenticated:
        
        goal = get_object_or_404(Goal, id=goal_id)
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
        record = get_object_or_404(record, id=record_id)
        if request.user == record.owner:
            comments = (Comment.objects.all().filter(record=record)
                               .order_by('-create_date'))
            return render(request, 'record/detail.html',
                          {'record': record, 'comments': comments})
    return redirect_home(request.user)
"""

def redirect_patient_list():
    return HttpResponseRedirect("/home/records/patient_list")


def redirect_record(patient_id, record_id):
    return HttpResponseRedirect("/home/records/patient/{}/record/{}".
                                format(patient_id, record_id))

def redirect_my_patient_records(patient_id):
    return HttpResponseRedirect("/home/records/patient/{}/my_records".format(patient_id))

def redirect_all_patient_records(patient_id):
    return HttpResponseRedirect("/home/records/{}".format(patient_id))
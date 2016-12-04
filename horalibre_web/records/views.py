from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from login.views import redirect_home
from .models import Patient, Record, Professional
from commentary.models import Comment

"""
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

def delete_record(request, record_id):
    record = get_object_or_404(record, pk=record_id)
    if request.user.is_authenticated:
        if request.user == record.owner:
            if request.method == "POST":
                record.delete()
                return redirect_home(request.user.username)
            else:
                return render(request, 'record/delete.html', {'record': record})
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

def modify_record(request, record_id):
    record = get_object_or_404(record, pk=record_id)
    if request.user.is_authenticated:
        if request.user == record.owner:
            if request.method == "POST":
                if request.POST.get("finish_date"):
                    record.finish_date = request.POST.get("finish_date")
                if request.POST.get("record_text"):
                    record.record_text = request.POST.get("record_text")
                if request.POST.get("create_date"):
                    record.create_date = request.POST.get("create_date")
                if request.POST.get("priority"):
                    record.priority = request.POST.get("priority")
                if request.POST.get("state"):
                    record.state = request.POST.get("state")
                record.save()
                return redirect_record(record_id)
            else:
                return render(request, 'record/modify_record.html', {'record': record})

"""

def redirect_record(record_id):
    return HttpResponseRedirect("/record/{}".format(record_id))

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.patient_list, name='patient_list'),
    url(r'^create_record$', views.create_record, name='create_record'),
    url(r'^(?P<patient_id>[0-9]+)/$',views.record_list,name='record_list'),
    url(r'^(?P<patient_id>[0-9]+)/create_record_from_patient$',views.create_record_from_patient,name='create_record_from_patient'),
    url(r'^(?P<patient_id>[0-9]+)/record/(?P<record_id>[0-9]+)/$',views.record_detail,name='record_detail'),
    url(r'^(?P<patient_id>[0-9]+)/record/(?P<record_id>[0-9]+)/edit$',views.edit_record,name='edit_record'),
    url(r'^(?P<patient_id>[0-9]+)/record/(?P<record_id>[0-9]+)/delete$',views.delete_record,name='delete_record'),
]

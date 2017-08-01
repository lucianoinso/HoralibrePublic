from django.conf.urls import url

from . import views
from commentary import views as comment_views

urlpatterns = [
    url(r'^send_notifications$', views.send_notifications, name='send_notifications'),
    url(r'^patient_list$', views.patient_list, name='patient_list'),
#    url(r'^create_record$', views.create_record, name='create_record'),
    url(r'^patient/(?P<patient_id>[0-9]+)/select_records$',views.select_records,name='select_records'),
    url(r'^patient/(?P<patient_id>[0-9]+)/all_records$',views.all_records_list,name='all_records_list'),
    url(r'^patient/(?P<patient_id>[0-9]+)/my_records$',views.my_records_list,name='my_records_list'),
    url(r'^patient/(?P<patient_id>[0-9]+)/create_record_from_patient$',views.create_record_from_patient,name='create_record_from_patient'),
    url(r'^patient/(?P<patient_id>[0-9]+)/record/(?P<record_id>[0-9]+)/$',views.record_detail,name='record_detail'),
    url(r'^patient/(?P<patient_id>[0-9]+)/record/(?P<record_id>[0-9]+)/edit$',views.edit_record,name='edit_record'),
    url(r'^patient/(?P<patient_id>[0-9]+)/record/(?P<record_id>[0-9]+)/delete$',views.delete_record,name='delete_record'),
    url(r'^patient/(?P<patient_id>[0-9]+)/record/(?P<record_id>[0-9]+)/new_comment$',comment_views.new_comment,name='new_comment'),
    url(r'^patient/(?P<patient_id>[0-9]+)/record/(?P<record_id>[0-9]+)/edit_comment/(?P<comment_id>[0-9]+)/$',comment_views.edit_comment,name='edit_comment'),
    url(r'^patient/(?P<patient_id>[0-9]+)/record/(?P<record_id>[0-9]+)/delete_comment/(?P<comment_id>[0-9]+)/$',comment_views.delete_comment,name='delete_comment'),
]

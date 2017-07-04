from django.conf.urls import url

from . import views
# from commentary import views as comment_views

urlpatterns = [
    url(r'^$', views.admin_home, name='admin_home'),
    # Profesionals
    url(r'^create/professional$', views.create_professional, name='create_professional'),
    url(r'^modify/professional$', views.modify_proff_menu, name='modify_proff_menu'),
    url(r'^modify/professional/(?P<proff_id>[0-9]+)$', views.modify_proff, name='modify_proff'),
    url(r'^delete/professional$', views.delete_professional, name='delete_professional'),
    # Secretary
    url(r'^create/secretary$', views.create_secretary, name='create_secretary'),
    url(r'^modify/secretary$', views.modify_secretary, name='modify_secretary'),
    url(r'^delete/secretary$', views.delete_secretary, name='delete_secretary'),
    # Patients
    url(r'^create/patient$', views.create_patient, name='create_patient'),
    url(r'^modify/patient$', views.modify_patient, name='modify_patient'),
    url(r'^delete/patient$', views.delete_patient, name='delete_patient'),
    # Cases
    url(r'^create/case$', views.create_case, name='create_case'),
    url(r'^modify/case$', views.modify_case, name='modify_case'),
    url(r'^delete/case$', views.delete_case, name='delete_case'),
    # url(r'^patient_list$', views.patient_list, name='patient_list'),
    # url(r'^create_record$', views.create_record, name='create_record'),
    # url(r'^patient/(?P<patient_id>[0-9]+)/select_records$',views.select_records,name='select_records'),
    # url(r'^patient/(?P<patient_id>[0-9]+)/all_records$',views.all_records_list,name='all_records_list'),
    # url(r'^patient/(?P<patient_id>[0-9]+)/my_records$',views.my_records_list,name='my_records_list'),
    # url(r'^patient/(?P<patient_id>[0-9]+)/create_record_from_patient$',views.create_record_from_patient,name='create_record_from_patient'),
    # url(r'^patient/(?P<patient_id>[0-9]+)/record/(?P<record_id>[0-9]+)/$',views.record_detail,name='record_detail'),
    # url(r'^patient/(?P<patient_id>[0-9]+)/record/(?P<record_id>[0-9]+)/edit$',views.edit_record,name='edit_record'),
    # url(r'^patient/(?P<patient_id>[0-9]+)/record/(?P<record_id>[0-9]+)/delete$',views.delete_record,name='delete_record'),
    # url(r'^patient/(?P<patient_id>[0-9]+)/record/(?P<record_id>[0-9]+)/new_comment$',comment_views.new_comment,name='new_comment'),
    # url(r'^patient/(?P<patient_id>[0-9]+)/record/(?P<record_id>[0-9]+)/edit_comment/(?P<comment_id>[0-9]+)/$',comment_views.edit_comment,name='edit_comment'),
    # url(r'^patient/(?P<patient_id>[0-9]+)/record/(?P<record_id>[0-9]+)/delete_comment/(?P<comment_id>[0-9]+)/$',comment_views.delete_comment,name='delete_comment'),
]

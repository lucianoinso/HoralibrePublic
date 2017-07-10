from django.conf.urls import url

from . import views
# from commentary import views as comment_views

urlpatterns = [
    url(r'^$', views.admin_home, name='admin_home'),
    # Profesionals
    url(r'^create/professional$', views.create_professional, name='create_professional'),
    url(r'^modify/professional$', views.modify_professional_menu, name='modify_professional_menu'),
    url(r'^modify/professional/(?P<prof_id>[0-9]+)$', views.modify_professional, name='modify_professional'),
    url(r'^delete/professional$', views.delete_professional, name='delete_professional'),
    # Secretary
    url(r'^create/secretary$', views.create_secretary, name='create_secretary'),
    url(r'^modify/secretary$', views.modify_secretary_menu, name='modify_secretary_menu'),
    url(r'^modify/secretary/(?P<secretary_id>[0-9]+)$', views.modify_secretary, name='modify_secretary'),
    url(r'^delete/secretary$', views.delete_secretary, name='delete_secretary'),
    # Patients
    url(r'^create/patient$', views.create_patient, name='create_patient'),
    url(r'^modify/patient$', views.modify_patient_menu, name='modify_patient_menu'),
    url(r'^modify/patient/(?P<patient_id>[0-9]+)$', views.modify_patient, name='modify_patient'),
    url(r'^delete/patient$', views.delete_patient, name='delete_patient'),
    # Cases
    url(r'^create/case$', views.create_case, name='create_case'),
    url(r'^modify/case$', views.modify_case_menu, name='modify_case_menu'),
    url(r'^modify/case/(?P<case_id>[0-9]+)$', views.modify_case, name='modify_case'),
    url(r'^delete/case$', views.delete_case, name='delete_case'),
]

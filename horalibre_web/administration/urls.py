from . import views
# from commentary import views as comment_views

urlpatterns = [
    url(r'^$', views.admin_home, name='admin_home'),
    # Profesionals
    url(r'^professional/(?P<prof_id>[0-9]+)$', views.professional_detail, name='professional_detail'),
    url(r'^list/professional$', views.list_professional, name='list_professional'),
    url(r'^create/professional$', views.create_professional, name='create_professional'),
    url(r'^modify/professional$', views.modify_professional_menu, name='modify_professional_menu'),
    url(r'^modify/professional/(?P<prof_id>[0-9]+)$', views.modify_professional, name='modify_professional'),
    url(r'^modify/professional/(?P<prof_id>[0-9]+)/change_password$', views.change_pwd_prof, name='change_pwd_prof'),
    url(r'^delete/professional$', views.delete_professional, name='delete_professional'),
    # Secretary
    url(r'^secretary/(?P<secretary_id>[0-9]+)$', views.secretary_detail, name='secretary_detail'),
    url(r'^list/secretary$', views.list_secretary, name='list_secretary'),
    url(r'^create/secretary$', views.create_secretary, name='create_secretary'),
    url(r'^modify/secretary$', views.modify_secretary_menu, name='modify_secretary_menu'),
    url(r'^modify/secretary/(?P<secretary_id>[0-9]+)$', views.modify_secretary, name='modify_secretary'),
    url(r'^modify/secretary/(?P<secretary_id>[0-9]+)/change_password$', views.change_pwd_secr, name='change_pwd_secr'),
    url(r'^delete/secretary$', views.delete_secretary, name='delete_secretary'),
    # Patients
    url(r'^patient/(?P<patient_id>[0-9]+)$', views.patient_detail, name='patient_detail'),
    url(r'^list/patient$', views.list_patient, name='list_patient'),
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

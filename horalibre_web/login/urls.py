from . import views

urlpatterns = [
    # /login
    url(r'^$', views.login, name='login'),
]

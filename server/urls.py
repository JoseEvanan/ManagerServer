from django.conf.urls import url

from server import views

app_name = 'server'

urlpatterns = [
    url(r'^manager_server/$', views.ManagerServerView.as_view(),
        name='manager_server'),
    url(r'^start_server/$', views.StartServerView.as_view(),
        name='start_server'),
    url(r'^stop_server/$', views.StopServerView.as_view(),
        name='stop_server'),
    url(r'^reset_server/$', views.ResetServerView.as_view(),
        name='reset_server'),
]
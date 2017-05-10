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
    url(r'^list_server/$', views.ListServerView.as_view(),
        name='list_server'),
    url(r'^save_server/$', views.SaveServerView.as_view(),
        name='save_server'),
    url(r'^detail_group/$', views.DetailGroupView.as_view(),
        name='detail_group'),
    url(r'^action_remove/$', views.RemovePermView.as_view(),
        name='action_remove'),
    url(r'^change_perm/$', views.ChangePermView.as_view(),
        name='change_perm'),
    
]


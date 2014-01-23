from django.conf.urls import patterns, url
from tracker import views

urlpatterns = patterns('', 
	url(r'^$', views.index, name='index'),
	url(r'^logout/$', views.logout_view, name="logout_view"),
    url(r'^login/$', views.login, name="login"),
	url(r'^john/$', views.john, name='john'),
	url(r'^thanks/$', views.thanks, name='thanks'),
    url(r'^created/$', views.created, name='created'),
	url(r'^create_session/$', views.create_session, name="create_session"),
	url(r'^(?P<session_id>\d+)/log_performance/$', views.log_performance, name='log_performance'),
    url(r'^(?P<session_id>\d+)/choose_slot/$', views.choose_slot, name='choose_slot')
)
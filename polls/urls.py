from django.conf.urls import url
from . import views

app_name = 'polls'
urlpatterns = [
	url(r'^login/$', views.login_auth, name='login_auth'),
	url(r'^logout/$', views.logoutView, name='logout'),
    url(r'^$', views.IndexView, name='index'),
    #url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    #url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
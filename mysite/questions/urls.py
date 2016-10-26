from django.conf.urls import url

from . import views

app_name = 'questions'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/answers/$', views.AnswersView.as_view(), name='answers'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),

]

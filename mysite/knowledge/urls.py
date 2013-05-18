 
from django.conf.urls import patterns, url

from knowledge import views

urlpatterns = patterns('',
    url(r'^$', views.nuevo_suceso, name='index')
)
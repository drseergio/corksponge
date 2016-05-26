# coding: utf-8
from django.conf.urls.defaults import include
from django.conf.urls.defaults import patterns
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    (r'^_ah/warmup$', 'djangoappengine.views.warmup'),
    (r'^admin/', include(admin.site.urls)))

urlpatterns += patterns('',
    (r'^$', 'corksponge.views.index'),
    (r'^save$', 'corksponge.views.save'),
    (r'^click$', 'corksponge.views.click'),
    (r'^delete$', 'corksponge.views.delete'),
    (r'^update$', 'corksponge.views.update'),
    (r'^(\w{6})$', 'corksponge.views.display'),
    (r'^get/(\w{6})$', 'corksponge.views.get'),
    (r'^\w+$', 'corksponge.views.index'))

urlpatterns += staticfiles_urlpatterns()

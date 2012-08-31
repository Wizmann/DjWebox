# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from views.register import *
from views.handshake import *
from views.login import *
from views.upload import *
from views.download import *
from views.getlist import *
from views.delete import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'DjWebox.views.home', name='home'),
    # url(r'^DjWebox/', include('DjWebox.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^(?i)admin/', include(admin.site.urls)),
    (r'^(?i)register/$', register),
    (r'^(?i)handshake/$',handshake),
    (r'^(?i)login/$',login),  
    (r'^(?i)upload/$',upload),
    (r'^(?i)download/$',download),
    (r'^(?i)getlist/$',getlist),
    (r'^(?i)delete/$',delete),
)

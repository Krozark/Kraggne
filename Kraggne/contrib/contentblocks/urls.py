# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url #,include
from Kraggne.contrib.contentblocks.views import AjaxRecieverView

urlpatterns = patterns('',
    url(r'^ajax-receiver',AjaxRecieverView.as_view(),name="ajax-receiver"),
)


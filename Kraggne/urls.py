# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls.defaults import patterns#, include, url
from Kraggne.views import GenericView
from Kraggne.models import MenuItem
from Kraggne.utils import MakePattern

urlpatterns = patterns('',)

for u in MenuItem.objects.filter(cms_page = True,is_visible=True):
    urlpatterns += MakePattern(u)

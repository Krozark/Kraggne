# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls.defaults import patterns#, include, url
from Kraggne.views import GenericView
from Kraggne.models import MenuItem
from Kraggne.utils import MakePattern
from django.db.models import Q

urlpatterns = patterns('',)

for u in MenuItem.objects.filter(Q(cms_page = True) &  Q(is_visible=True) & ~Q(url__startswith='include(') | Q(view__startswith='detail(')):
    urlpatterns += MakePattern(u)

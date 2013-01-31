# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls.defaults import patterns#, include, url
from django.db.models import Q
from django.conf.urls.defaults import url,include

from Kraggne.views import GenericView
from Kraggne.models import MenuItem
from Kraggne.utils import MakePattern


urlpatterns = patterns('',
   url(r'^contentblocks/', include("Kraggne.contrib.contentblocks.urls")),
)

for u in MenuItem.objects.filter(Q(cms_page = True)):
    urlpatterns += MakePattern(u)

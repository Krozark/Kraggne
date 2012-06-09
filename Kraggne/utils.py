# -*- coding: utf-8 -*-
from Kraggne.views import GenericView
from django.conf.urls.defaults import patterns,url

def MakePattern(menuItem):
    ur = menuItem.url

    if ur == "/":
        ur=""
    else:
        if ur[0] == "/" and len(ur)>1:
            ur = ur[1:]
        if len(ur)>1 and ur[-1] != "/":
            ur+="/"
    if ur[0] == '^':
        ur = ur[1:]
    if ur[-1] == '$':
        ur= ur[:-1]
    return patterns('',url(
                r'^%s$' % ur,
                GenericView.as_view(),
                kwargs={"pk": menuItem.pk,},
                name="kraggne-%s" % menuItem.slug
                ))

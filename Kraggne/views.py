# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
#from django.http import HttpResponseRedirect, HttpResponse
#from django.core.context_processors import csrf

#from django.template.context import RequestContext# Context
from django.utils.translation import ugettext_lazy as _
#from django.db.models import Q

from Kraggne.models import MenuItem

class GenericView(TemplateView):
    template_name = "Kraggne/genericPage.html"

    def get_context_data(self, **kwargs):
        context = super(GenericView, self).get_context_data(**kwargs)

        page =  kwargs.get('page',False)
        if page:
            context['page'] = page

            #content = ItemPage.objects.filter(parent__slug=slug).order_by('')
            #print content
            #context['content_blocks'] = content
        return context

#from django.shortcuts import render_to_response
#def Generic(request,*args,**kwargs):
#    return ''

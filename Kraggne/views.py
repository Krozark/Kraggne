# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
#from django.http import HttpResponseRedirect, HttpResponse
#from django.core.context_processors import csrf

#from django.template.context import RequestContext# Context
from django.utils.translation import ugettext_lazy as _
#from django.db.models import Q

from Kraggne.models import MenuItem

class GenericView(TemplateView):
    template_name = "Karggne/genericPage.html"

    def get_context_data(self, **kwargs):
        context = super(GenericView, self).get_context_data(**kwargs)

        pk =  kwargs['params'].get('pk',False)
        if not pk:
            pk =  kwargs.get('pk',False)
        if pk:
            page = MenuItem.objects.get(pk=pk)
            context['page_slug'] = page.slug
            content = ItemPage.objects.filter(parent__slug=slug).order_by('')
            print content
            context['content_blocks'] = content
        return context

#from django.shortcuts import render_to_response
#def Generic(request,*args,**kwargs):
#    return ''

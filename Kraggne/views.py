# -*- coding: utf-8 -*-
from django.views.generic import TemplateView, FormView
#from django.http import HttpResponseRedirect, HttpResponse
#from django.core.context_processors import csrf

#from django.template.context import RequestContext# Context
from django.utils.translation import ugettext_lazy as _
#from django.db.models import Q

from Kraggne.models import MenuItem

def addSelfToContext(slug,context):
    try:
        context['page'] = MenuItem.objects.get(slug=slug)
    except:
        pass

class GenericViewContextMixinSlug(object):
    slug = ''
    def get_context_data(self, **kwargs):
        context = super(GenericViewContextMixinSlug, self).get_context_data(**kwargs)
        addSelfToContext(self.slug,context)
        return context


class GenericViewContextMixin(object):
    def get_context_data(self, **kwargs):
        context = super(GenericViewContextMixin, self).get_context_data(**kwargs)

        page =  self.kwargs.get('page',False)
        if page:
            context['page'] = page

        return context


class GenericView(GenericViewContextMixin,TemplateView):
    template_name = "Kraggne/genericPage.html"

    #def __init__(self,page):
    #    self.test = page.url

from django.http import HttpResponseRedirect
class GenericFormView(FormView):

    template_name = "Kraggne/genericFormPage.html"

    def get_form(self,form_class=None):
        try:
            return self.kwargs.get('page').formblock.getFormClass()
        except:
            return super(GenericFormView,self).get_form(form_class)

    def post(self,request,*args,**kwargs):
        form = self.get_form()(request.POST)
        if form.is_valid():
            self.object = form.save()
            page = self.kwargs['page']
            return HttpResponseRedirect(page.formblock.url or page.url)
        return self.render_to_response(self.get_context_data(form=form))


        #return self.kwargs.get('page').formblock.getFormClass()

    def get_context_data(self, **kwargs):
        context = super(GenericFormView, self).get_context_data(**kwargs)

        page =  self.kwargs.get('page',False)
        for u in kwargs:
            context[u] = kwargs[u]
        if page:
            context['page'] = page

        self.success_url = page.formblock.url or page.url
        if page.url[-1] != "/":
            context['action_url'] = page.url + "/"
        else:
            context['action_url'] = page.url

        return context


#from django.shortcuts import render_to_response
#def Generic(request,*args,**kwargs):
#    return ''

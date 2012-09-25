# -*- coding: utf-8 -*-
from django.views.generic import TemplateView, FormView, ListView
#from django.http import HttpResponseRedirect, HttpResponse
#from django.core.context_processors import csrf

#from django.template.context import RequestContext# Context
from django.utils.translation import ugettext_lazy as _
#from django.db.models import Q

from Kraggne.models import MenuItem
from Kraggne.contrib.flatblocks.utils import GetTemplatesPath
from django.http import Http404

def addSelfToContext(slug,context):
    try:
        page = MenuItem.objects.get(slug=slug)
        context['page'] = page
        for u in page.pagevar_set.all():
            u.addToContext(context)
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

        for u in page.pagevar_set.all():
            u.addToContext(context)

        context.pop('params')
        return context


class GenericView(GenericViewContextMixin,TemplateView):
    template_name = "Kraggne/genericPage.html"

    #def __init__(self,page):
    #    self.test = page.url

class GenericDetailView(GenericView):
    template_name = "Kraggne/genericDetailPage.html"
    model = None

    def get_for_object(self,**kwargs):
        obj = None
        if hasattr(self.model,'get_object_from_url'):
            obj = self.model.get_object_from_url(**kwargs)
        #by pk
        pk = kwargs.get('pk')
        if not obj and pk:
            r =self.model.objects.filter(pk=pk)
            obj = r and r[0] or None
        #by slug
        if not obj:
            slug = kwargs.get('slug')
            if slug:
                r =self.model.objects.filter(slug=slug)
                obj = r and r[0] or None
        return obj

    def get_template_names(self):
        names = []
        if hasattr(self.model, '_meta'):
            names.append("%s/%s/detail.html" % (
                self.model._meta.app_label,
                self.model._meta.object_name.lower(),
            ))

        names.append(self.template_name)
        return names
    

    def get_context_data(self, **kwargs):
        context = super(GenericDetailView, self).get_context_data(**kwargs)
        context['object'] = self.get_for_object(**kwargs)
        return context

from django.http import HttpResponseRedirect
class GenericFormView(FormView):

    template_name = "Kraggne/genericFormPage.html"

    def get_context_data(self, **kwargs):
        context = super(GenericFormView, self).get_context_data(**kwargs)
        
        page =  self.kwargs.get('page',False)
        if page:
            context['page'] = page

        self.success_url = page.formblock.url or page.url
        if page.url[-1] != "/":
            context['action_url'] = page.url + "/"
        else:
            context['action_url'] = page.url

        return context

class GenericListView(ListView):

    template_name = "Kraggne/genericListPage.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(GenericListView, self).get_context_data(**kwargs)

        page =  self.kwargs.get('page',False)
        if page:
            context['page'] = page

        return context

    def paginate_queryset(self, queryset, page_size):
        paginator = self.get_paginator(queryset, page_size, allow_empty_first_page=self.get_allow_empty())
        page = self.request.GET.get('page') or 1
        try:
            page_number = int(page)
        except ValueError:
            if page == 'last':
                page_number = paginator.num_pages
            else:
                raise Http404(_(u"Page is not 'last', nor can it be converted to an int."))
        try:
            page = paginator.page(page_number)
            return (paginator, page, page.object_list, page.has_other_pages())
        except InvalidPage:
            raise Http404(_(u'Invalid page (%(page_number)s)') % {
                'page_number': page_number
            })


    def get_paginate_by(self, queryset):
        if hasattr(self.model, 'paginate_by'):
            return self.model.paginate_by
        return self.paginate_by

    def get_template_names(self):
        names = []
        if hasattr(self.model, '_meta'):
            names.append("%s/%s/list.html" % (
                self.model._meta.app_label,
                self.model._meta.object_name.lower(),
            ))

        names.append(self.template_name)
        return names

#from django.shortcuts import render_to_response
#def Generic(request,*args,**kwargs):
#    return ''

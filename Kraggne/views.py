# -*- coding: utf-8 -*-
from django.views.generic import TemplateView, FormView, ListView
from django.views.generic.edit import ProcessFormView, FormMixin
from django import forms
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


class GenericViewContextMixin(GenericViewContextMixinSlug):
    def get_context_data(self, **kwargs):
        context = super(GenericViewContextMixin, self).get_context_data(**kwargs)

        page =  self.kwargs.get('page',False)
        if page:
            context['page'] = page
        else:
            return context

        for u in page.pagevar_set.all():
            u.addToContext(context)

        try:
            context.pop('params')
        except:
            pass

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
        try:
            context["object_model_name"] = "%s.%s" % (self.model._meta.app_label.lower(),self.model._meta.object_name.lower())
        except:
            pass
        return context

from django.http import HttpResponseRedirect
class GenericFormView(GenericViewContextMixin,FormView):

    template_name = "Kraggne/genericFormPage.html"
    #success_url = None

    def get_success_url(self):
        if self.slug:
            page = MenuItem.objects.filter(slug=self.slug)[:1]
            if page:
                try:
                    return page[0].formblock.url
                except:
                    return page[0].url

        if self.page:
            try:
                return self.page.formblock.url
            except:
                return self.page.url
        return None

    def get_context_data(self, **kwargs):
        context = super(GenericFormView, self).get_context_data(**kwargs)
        
        page =  self.kwargs.get('page',False)
        if page:
            context['page'] = page

        #self.success_url = page.formblock.url or page.url
        if page.url[-1] != "/":
            context['action_url'] = page.url + "/"
        else:
            context['action_url'] = page.url

        return context

class GenericListView(GenericViewContextMixin,ListView):

    template_name = "Kraggne/genericListPage.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(GenericListView, self).get_context_data(**kwargs)

        page =  self.kwargs.get('page',False)
        if page:
            context['page'] = page

        try:
            context["object_model_name"] = "%s.%s" % (self.model._meta.app_label.lower(),self.model._meta.object_name.lower())
        except:
            pass

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

class GenericListFormView(GenericListView,FormMixin,ProcessFormView):
    template_name = "Kraggne/genericFormPage.html"

    def get_context_data(self,form=None,**kwargs):
        context = GenericListView.get_context_data(self,**kwargs)
        
        if not form:
            form_class = self.get_form_class()
            form = self.get_form(form_class)
        context["form"] = form

        page = context["page"]
        if page.url[-1] != "/":
            context['action_url'] = page.url + "/"
        else:
            context['action_url'] = page.url

        return context

    def post(self,request,*args,**kwarg):
        self.page = kwarg.pop('page')
        return ProcessFormView.post(self,request,*args,**kwarg)

    def is_model_form(self):
        return issubclass(self.get_form_class(),forms.ModelForm)

    def get_success_url(self):
        if hasattr(self,'object') and self.object is not None and hasattr(self.object,'get_absolute_url'):
            return self.object.get_absolute_url()
        if self.slug:
            page = MenuItem.objects.filter(slug=self.slug)[:1]
            if page:
                try:
                    return page[0].formblock.url
                except:
                    return page[0].url

        if self.page:
            try:
                return self.page.formblock.url
            except:
                return self.page.url
        return None

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instanciating the form.
        """
        kwargs = FormMixin.get_form_kwargs(self)
        if hasattr(self,'object'):
            kwargs.update({'instance': self.object})
        return kwargs


    def form_valid(self,form):
        if self.is_model_form():
            try:
                self.object = form.save(commit=True,request=self.request)
            except TypeError:
                self.object = form.save(commit=True)
            #if hasattr(self.object,'save_model'):
            #    self.object.save_model(self.request,form,False):
        return FormMixin.form_valid(self,form)

    def form_invalid(self,form):
        self.object_list = self.get_queryset()
        return self.render_to_response(self.get_context_data(form=form,object_list=self.object_list))



#from django.shortcuts import render_to_response
#def Generic(request,*args,**kwargs):
#    return ''

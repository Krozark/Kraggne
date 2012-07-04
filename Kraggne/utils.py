# -*- coding: utf-8 -*-
from Kraggne.views import GenericView, GenericFormView
from django.conf.urls.defaults import patterns,url
from django.utils.translation import ugettext_lazy as _
from django.db.models.loading import get_model

def MakePattern(menuItem):
    ur = menuItem.url
    if len(ur) > 0:
        if ur == "/":
            ur=""
        else:
            if ur[0] == "/" and len(ur)>1:
                ur = ur[1:]
            if len(ur)>1 and ur[-1] != "/":
                ur+="/"
        if len(ur) and ur[0] == '^':
            ur = ur[1:]
        if len(ur) and ur[-1] == '$':
            ur= ur[:-1]

    q={}
    try:
        m = menuItem.formblock
        view = GenericFormView
        q['form_class'] = m.getFormClass()
    except:# Exception,e:
        #print e
        view = GenericView

    try :
        t = menuItem.pagetemplate
        q['template_name'] = t.template_path
    except :
        pass

    view = view.as_view(**q)


    return patterns('',url(
                r'^%s$' % ur,
                view,
                kwargs={"page": menuItem,},
                name="kraggne-%s" % menuItem.slug
                ))


from django.test.client import Client
from django.forms import ValidationError
from django.core.urlresolvers import reverse, NoReverseMatch
import re

def clean_include_url(link,include): #include(app.model)
#return link
    if link.startswith("include(") and include:
        app = link[len('include('):]
        app = app.split('.').replace(')','')
        if len(app) != 2:
            raise ValidationError(_('imposible to find "." syntax: include(app.model)'))

        app,model = app[0],app[1]

        m = get_model(app,model)

        if not m:
            raise ValidationError(_('No model find %s.%s' % (app,model)))
        try:
            m.get_absolute_url()
        except TypeError:
            return link,link
        raise ValidationError(_('model %s.%s has no get_absolute_url(self) function' % (app,model)))
    return link

def clean_detail_url(link,detail): #detail(url,app.model) (slug or pk in url) else (app.get_objetct_from_url(**kwargs))
#return link, modelclass, 0 if basic (slug or pk) 1 if custom (model.get_objetct_from_url(**kwargs))
    if link.startswith("detail(") and detail:
        url = link[len('detail('):]
        i = url.rfind(',')
        if i <=0:
            raise ValidationError(_('imposible to find "," syntaxe: detail(url,app.model)'))
        
        app = link[i+1:].replace(')','')
        url = link[:i].replace('"','').replace("'",'')
        app = app.split('.')

        if len(app) != 2:
            raise ValidationError(_('imposible to find one "." in %s syntaxe: detail(url,app.model)' % '.'.join(app)))

        app,model = app[0],app[1]

        m = get_model(app,model)
        if not m:
            raise ValidationError(_('No model find %s.%s' % (app,model)))

        try:
            r = re.compile(link)
        except Exception, e:
            raise ValidationError(_('Please supply a valid regex URL. %s' % e))

        if len(r.groupindex) == 1:
            if not ('pk' in r.groupindex or 'slug' in r.groupindex):
                raise ValidationError(_('Please supply a valid regex URL. with <pk> OR <slug> '))

            if 'slug' in groupindex and no hasattr(m,'slug'):
                raise ValidationError(_("'<slug> is define in URL, but your model has no attr 'slug'"))
            return link,m,0
        raise ValidationError(_('Please supply a valid regex URL. with <pk> or <slug>. You can also define a get_object_from_url(***kwargs) method in your model. This methode must return a object' % (app,model)))
    return link

def clean_url(link,include=False,hashtags = True,gettag=True):
    url = None
    if link[0] == "/": #a defined URL
        c = Client()
        try:
            resp = c.get(link)
            if resp.status_code == 404:
                raise ValidationError(_(u'%s is not a local URL (does not exist)' % link))
            url = link.strip()
            if len(url) == 0:
                url ="/"
            return link,url
        except:
            raise ValidationError(_(u'%s is not a local URL (not a valid URL)' % link))

    elif link[0] != '^' : # Not a regex or site-root-relative absolute path
        hash = ''
        if '#' in link and hashtags:
            i = link.find('#')
            hash = link[i:]
            link = link[:i]
        get = ''
        if '?' in link and gettag:
            i = link.find('?')
            get = link[i:]
            link = link[:i]
        
        link = clean_include_url(link,include)

        try: # named URL or view
            print link
            url = reverse(link)
            if len(url) == 0:
                url ="/"
            return link +get+ hash,url+get+ hash
        except NoReverseMatch:
            raise ValidationError(_('No view find to reverse the url %s' % link))
    elif link[0] == '^': #regex
        raise ValidationError(_('Regex are not suported with redirect url. Please use named url insted'))
    if len(url) == 0:
        url ="/"
    return link +get+ hash,url +get+ hash


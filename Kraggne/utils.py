# -*- coding: utf-8 -*-
import Kraggne.views as _view
#import GenericView, GenericFormView, GenericDetailView, GenericListView
from django.conf.urls.defaults import patterns,url
from django.utils.translation import ugettext_lazy as _
from django.db.models.loading import get_model
from django.contrib.auth.decorators import login_required
from Kraggne.decorators import login_forbidden
from Kraggne.parser import get_model_and_url_from_detail,get_model_from_include,  get_model_and_url_from_list

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
    c = "Generic"
    if menuItem.is_detail():
        #view = _view.GenericDetailView
        q['model'] = menuItem._get_for_detail_model()
        c += "Detail"
    elif menuItem.is_list():
        #view = _view.GenericListView
        q['model'] = menuItem._get_for_list_model()
        c += "List"
    try:
        m = menuItem.formblock
        q['form_class'] = m.getFormClass()
        c+= "Form"
    except:# Exception,e:
        pass

    c += "View"

    view = getattr(_view,c)

    try :
        t = menuItem.pagetemplate
        q['template_name'] = t.template_path
    except :
        pass

    v = None
    if menuItem.login_required:
        view = login_required(view.as_view(**q))
        v= True
    if menuItem.login_forbidden:
        view = login_forbidden(view.as_view(**q))
        v = True
    if not v:
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
#return link,url,status
    if link.startswith("include(") and include:
        m, app, model = get_model_from_include(link,return_app_model=True)

        if not m:
            raise ValidationError(_('No model find %s.%s' % (app,model)))

        if hasattr(m,'get_absolute_url'):
            return link,link,True

        raise ValidationError(_('model %s.%s has no get_absolute_url(self) function' % (app,model)))
    return link,link,None

def clean_detail_url(link,detail): #detail(url,app.model) (slug or pk in url) else (app.get_objetct_from_url(**kwargs))
#return link,url,status
    if link.startswith("detail(") and detail:
        m,url,app,model = get_model_and_url_from_detail(link,return_app_model=True)
        if not m:
            raise ValidationError(_('No model find %s.%s' % (app,model)))

        try:
            r = re.compile(url)
        except Exception, e:
            raise ValidationError(_('Please supply a valid regex URL. %s' % e))

        if r.groups == 1:
            if not ('pk' in r.groupindex or 'slug' in r.groupindex):
                raise ValidationError(_('Please supply a valid regex URL. with (?P<pk>[\d]+) OR (?P<slug>[-\w]+)'))

            if 'slug' in r.groupindex and not hasattr(m,'slug'):
                raise ValidationError(_("'<slug> is define in URL, but your model has no attr 'slug'"))
            return link,url,True

        if not hasattr(m,'get_object_from_url'):
            raise ValidationError(_('Please supply a valid regex URL. with <pk> or <slug>. You can also define a get_object_from_url(**kwargs) method in %s.%s if you want to use other(s) kwargs. This methode must return a object' % (app,model)))
        return link,url
    return link,link,None

def clean_list_url(link,lis=True):
    if link.startswith("list(") and lis:
        m,url,app,model = get_model_and_url_from_list(link,return_app_model=True)
        if not m:
            raise ValidationError(_('No model find %s.%s' % (app,model)))

        return link,url,True
    return link,link,None


def clean_url(link,include=False,detail=False,lis=False,hashtags = True,gettag=True,existe=True):
    url = None
    if link[0] == "/" and existe: #a defined URL
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
        hextra = ''
        hash = ''
        if '#' in link and hashtags:
            i = link.rfind('#')
            hash = link[i:]
            link = link[:i]
        get = ''
        if '(' in link:
            pass
            #a = link.rfind(')')
            #after_link = link[a+1:]
            #i = after_link.rfind('?')
            #if i >=0:
            #    get = after_link[i:]
            #    link = link[:a+1]
        else:
            if '?' in link and gettag :
                i = link.rfind('?')
                get = link[i:]
                link = link[:i]
        hextra = get+hash
        
        l,u,s = clean_include_url(link,include)
        if s: #ok for include()
            return l+hextra , u+hextra
        l,u,s = clean_detail_url(link,detail)
        if s: #ok for detail()
            return l+hextra , u+hextra
        l,u,s = clean_list_url(link,lis)
        if s: #ok for list()
            return l+hextra , u+hextra

        #No 'hacks'
        if existe:
            try: # named URL or view
                url = reverse(link)
                if len(url) == 0:
                    url ="/"
                return link +hextra,url+hextra
            except NoReverseMatch:
                raise ValidationError(_('No view find to reverse the url %s' % link))
        else:
            url = link
    if link[0] == '^': #regex
        raise ValidationError(_('Regex are not suported with redirect url. Please use named url insted'))
    if len(url or '') == 0:
        url ="/"
    return link +hextra,url +hextra


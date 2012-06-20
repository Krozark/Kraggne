# -*- coding: utf-8 -*-
from Kraggne.views import GenericView, GenericFormView
from django.conf.urls.defaults import patterns,url
from django.utils.translation import ugettext_lazy as _
from django.db.models.loading import get_model

def MakePattern(menuItem):
    ur = menuItem.url

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

    try:
        menuItem.formblock
        view = GenericFormView
    except:
        view = GenericView


    return patterns('',url(
                r'^%s$' % ur,
                view.as_view(),
                kwargs={"page": menuItem,},
                name="kraggne-%s" % menuItem.slug
                ))


from django.test.client import Client
from django.forms import ValidationError
from django.core.urlresolvers import reverse, NoReverseMatch
def clean_url(link,include=False,hashtags = True):
    url = None
    if link[0] == "/": #a defined URL
        c = Client()
        try:
            resp = c.get(link)
            if resp.status_code == 404:
                raise ValidationError(_(u'%s is not a local URL (does not exist)' % link))
            url = link
            return link,url
        except:
            raise ValidationError(_(u'%s is not a local URL (not a valid URL)' % link))

    elif link[0] != '^' : # Not a regex or site-root-relative absolute path
        hash = ''
        if '#' in link and hashtags:
            print "#"
            i = link.find('#')
            hash = link[i:]
            link = link[:i]
        if link.startswith("include(") and include:
            app = link[len('include('):]
            app , model = app.split('.')
            model = model.replace(')','')
            m = get_model(app,model)

            if not m:
                raise ValidationError(_('No model find %s.%s' % (app,model)))
            try:
                m.get_absolute_url()
            except TypeError:
                return link,link
            raise ValidationError(_('model %s.%s has no get_absolute_url(self) function' % (app,model)))



        try: # named URL or view
            url = reverse(link)
            return link + hash,url + hash
        except NoReverseMatch:
            raise ValidationError(_('No view find to reverse the url %s' % link))
    elif link[0] == '^': #regex
        raise ValidationError(_('Regex are not suported with redirect url. Please use named url insted'))
    return link + hash,url + hash

#from django.core.cache import cache
#def clearCache():
# try:
# cache._cache.clear() # in-memory caching
# except AttributeError:
# # try filesystem caching next
# old = cache._cull_frequency
# old_max = cache._max_entries
# cache._max_entries = 0
# cache._cull_frequency = 1
# cache._cull()
# cache._cull_frequency = old
# cache._max_entries = old_max

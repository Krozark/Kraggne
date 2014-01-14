# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db.models.loading import get_model
from django.forms import ValidationError

def get_model_from_include(link,return_app_model=False):
    app = link[len('include('):]
    app = app[:-1].split('.')
    if len(app) != 2:
        raise ValidationError(_('imposible to find "." syntax: include(app.model)'))

    app,model = app[0],app[1]

    if return_app_model:
        return get_model(app,model),app,model
    return get_model(app,model)

def get_model_and_url_from(prefix,link,return_app_model=False):
    url = link[len(prefix+"("):]
    i = url.rfind(',')
    if i <=0:
        raise ValidationError(_('imposible to find "," syntaxe: %s(url,app.model)' % prefix))
     
    app = url[i+1:].replace(')','')
    url = url[:i].replace('"','').replace("'",'')
    app = app.split('.')

    if len(app) != 2:
        raise ValidationError(_('imposible to find one "." in %s syntaxe: %s(url,app.model)' % ('.'.join(app),prefix)))

    app,model = app[0],app[1]

    if return_app_model:
        return get_model(app,model),url,app,model
    return get_model(app,model),url


def get_model_and_url_from_detail(link,return_app_model=False):
    return get_model_and_url_from("detail",link,return_app_model)

def get_model_and_url_from_list(link,return_app_model=False):
    return get_model_and_url_from("list",link,return_app_model)

def get_model_and_url_from_form(link,return_app_model=False):
    return get_model_and_url_from("form",link,return_app_model)

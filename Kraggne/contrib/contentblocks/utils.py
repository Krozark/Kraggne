# -*- coding: utf-8 -*-

from Kraggne.contrib.contentblocks.conf.settings import CONTENT_CHOICE_MODELS, CONTENT_FORM_MODELS
from django.contrib.contenttypes.models import ContentType
from django import forms

def get_content_choice_models():
    if CONTENT_CHOICE_MODELS:
        q = ContentType.objects.filter(pk=-1)#imposible, but it for be concatenate

        for u in CONTENT_CHOICE_MODELS:
            if not "app_label" in u:
                continue
            elif not "model" in u:
                q = q | ContentType.objects.filter(app_label = u["app_label"])
            else:
                if isinstance(u["model"],(dict,list,tuple)):
                    q = q | ContentType.objects.filter(app_label = u["app_label"],model__in = u["model"])
                else:
                    q = q | ContentType.objects.filter(app_label = u["app_label"],model = u["model"])
    else:
        q = ContentType.objects.all()

    return q
    

def model_to_modelform(model):
    try:
        form = CONTENT_FORM_MODELS[model._meta.app_label][model._meta.module_name]
        point = form.rfind('.')
        if point != -1:
            app = form[:point]
            klass = form[point+1:]
            f= __import__(app,globals(),locals(),[klass,])
            modelform_class=getattr(f,klass)
        else:
            modelform_class=__import__(form)
    except:
        meta = type('Meta', (), { "model":model, })
        modelform_class = type('modelform', (forms.ModelForm,), {"Meta": meta})
    return modelform_class



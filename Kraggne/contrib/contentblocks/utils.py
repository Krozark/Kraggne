# -*- coding: utf-8 -*-

from Kraggne.contrib.contentblocks.conf.settings import CONTENT_CHOICE_MODELS
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

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
    #q = ContentType.objects.filter(**kwargs).query
    

# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

CONTENT_CHOICE_MODELS = getattr(settings, "CONTENTBLOCKS_CONTENT_CHOICE_MODELS",
    (
        {
            "app_label" : "flatblocks",
            "model" : ("genericflatblocklist","templateblock")
        },
        {"app_label" : "gblocks",},
    )
)

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
        {
            "app_label" : "contentblocks",
            "model" : "pagecontaineur",
        }
    )
)

CONTENT_FORM_MODELS = getattr(settings, "CONTENTBLOCKS_CONTENT_FORM_MODELS",
{
    "flatblocks" : {
        "genericflatblocklist" : "Kraggne.contrib.flatblocks.forms.GenericFlatblockListForm",
        "templateblock" : "Kraggne.contrib.flatblocks.forms.TempateBlockForm"
    },
})


IMG_EXT_CHOICE = getattr(settings, "CONTENTBLOCKS_IMG_EXT_CHOICE",
    (
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".bmp"
    )
)

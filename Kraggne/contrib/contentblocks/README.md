need  Kraggne.contrib.flatblocks in your INSTALL_APPS, and to be put before Kraggne in it::

    INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'Kraggne.contrib.contentblocks',
    'Kraggne.contrib.flatblocks',
    'Kraggne.contrib.gblocks',
    'Kraggne',
    )

Options:
=======

block that can be create
CONTENTBLOCKS_CONTENT_CHOICE_MODELS default:
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

form asociate with CONTENTBLOCKS_CONTENT_CHOICE_MODELS models
CONTENTBLOCKS_CONTENT_FORM_MODELS default:
    {
        "flatblocks" : {
            "genericflatblocklist" : "Kraggne.contrib.flatblocks.forms.GenericFlatblockListForm",
            "templateblock" : "Kraggne.contrib.flatblocks.forms.TempateBlockForm"
        },
    }


image extantions
CONTENTBLOCKS_IMG_EXT_CHOICE default:
    (
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".bmp"
    )

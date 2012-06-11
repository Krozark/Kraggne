from django.conf import settings
from django.contrib import admin
from django_generic_flatblocks.contrib.gblocks.models import *

GRPAPPELLI_TINYMCE      = getattr(settings, 'GBLOCK_GRPAPPELLI_TINYMCE', False)
GRPAPPELLI_TINYMCE_SRC  = getattr(settings, 'GBLOCK_GRPAPPELLI_TINYMCE_SRC',  'grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js')
GRPAPPELLI_TINYMCE_CONF = getattr(settings, 'GBLOCK_GRPAPPELLI_TINYMCE_CONF', 'website/js/tinymce_setup.js')

if GRPAPPELLI_TINYMCE:
    GBLOCK_JS = [
        '%s%s' % (settings.STATIC_URL, GRPAPPELLI_TINYMCE_SRC),
        '%s%s' % (settings.STATIC_URL, GRPAPPELLI_TINYMCE_CONF)]
else:
    GBLOCK_JS = []

if 'grappellifit' in settings.INSTALLED_APPS and 'modeltranslation' in settings.INSTALLED_APPS:
    from grappellifit.admin import TranslationAdmin

    class GblockAdmin(TranslationAdmin):
        class Media:
            # FIXME: This might clash with TranslationAdmin.Media.js ..
            js = GBLOCK_JS
else:

    class GblockAdmin(admin.ModelAdmin):
        class Media:
            js = GBLOCK_JS
    

admin.site.register(Title, GblockAdmin)
admin.site.register(Text, GblockAdmin)
admin.site.register(Image)
admin.site.register(ImageAndLink, GblockAdmin)
admin.site.register(TitleAndFile, GblockAdmin)
admin.site.register(TitleTextAndFile, GblockAdmin)
admin.site.register(TitleAndText, GblockAdmin)
admin.site.register(TitleTextAndImage, GblockAdmin)
admin.site.register(TitleLinkAndImage, GblockAdmin)
admin.site.register(TitleLinkTextAndImage, GblockAdmin)

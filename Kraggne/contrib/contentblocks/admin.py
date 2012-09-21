# -*- coding: utf-8 -*-

from django.contrib import admin
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from Kraggne.contrib.contentblocks.models import PageObject, PageContaineur, ContaineurToObject

if 'grappellifit' in settings.INSTALLED_APPS and 'modeltranslation' in settings.INSTALLED_APPS:
    from grappellifit.admin import TranslationAdmin, TranslationStackedInline
    ADMIN = TranslationAdmin
    ADMIN_TAB = TranslationStackedInline
else:
    ADMIN = admin.ModelAdmin
    ADMIN_TAB = admin.TabularInline

############################################################
class PageContaineurAdmin(ADMIN):
    list_display = ("__unicode__",'page','position','hextra_class')
    list_filter = ('page',)
admin.site.register(PageContaineur,PageContaineurAdmin)

class PageObjectAdmin(ADMIN):
    list_display = ('related_object_changelink', "__unicode__")
    list_display_links = ('__unicode__',)

    def related_object_changelink(self, obj):
        return '<a href="%s"> %s - %s</a>' % (
            self.generate_related_object_admin_link(obj.content_object),
            "content",
            obj.content_object.__unicode__(),
        )

    related_object_changelink.allow_tags = True
    related_object_changelink.short_description = _('change related object')

    def generate_related_object_admin_link(self, related_object):
        return '../../%s/%s/%s/' % (
            related_object._meta.app_label,
            related_object._meta.module_name,
            related_object.pk
        )

    def change_view(self, request, object_id, extra_context=None):
        """
        Haven't figured out how to edit the related object as an inline.
        This template adds a link to the change view of the related
        object..
        """
        related_object = self.model.objects.get(pk=object_id).content_object
        c = {
            'admin_url': self.generate_related_object_admin_link(related_object),
            'related_object': related_object,
            'related_app_label': related_object._meta.app_label,
            'related_module_name': related_object._meta.module_name,
        }
        c.update(extra_context or {})
        self.change_form_template = 'admin/contentblocks/change_form_forward.html'
        return super(PageObjectAdmin, self).change_view(request, object_id, extra_context=c)

admin.site.register(PageObject,PageObjectAdmin)


class ContaineurToObjectAdmin(ADMIN):
    list_display = ("page_object","page_containeur","position")
admin.site.register(ContaineurToObject,ContaineurToObjectAdmin)

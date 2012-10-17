# -*- coding: utf-8 -*-

from django.contrib import admin
from Kraggne.forms import MenuItemForm, FormBlockForm
from Kraggne.models import MenuItem,FormBlock, PageTemplate, PageVar #PageBlock,
from django.conf import settings

if 'grappellifit' in settings.INSTALLED_APPS and 'modeltranslation' in settings.INSTALLED_APPS:
    from grappellifit.admin import TranslationAdmin, TranslationStackedInline
    ADMIN = TranslationAdmin
    ADMIN_TAB = TranslationStackedInline
else:
    ADMIN = admin.ModelAdmin
    ADMIN_TAB = admin.TabularInline

#################### INLINES ################################
class SubMenuItemInline(ADMIN_TAB):
    model = MenuItem
    extra = 1
    form = MenuItemForm
    prepopulated_fields = {'slug':('name',)}

class FormBlockInline(ADMIN_TAB):
    model = FormBlock
    extra = 0
    form = FormBlockForm

#class ItemPageInline(admin.TabularInline):
#    model = ItemPage
#    extra = 1
#    form = ItemPageForm


############################################################
class MenuItemAdmin(ADMIN):
    list_display = ('name','slug','order','view','url','parent','level','is_visible','cms_page','login_required','login_required_to_see')
    list_filter = ('is_visible','cms_page','login_required',"login_required_to_see")
    prepopulated_fields = {'slug':('name',)}
    form = MenuItemForm
    #inlines = [ItemPageInline,SubMenuItemInline]
    #inlines = [SubMenuItemInline,FormBlockInline]

    def queryset(self, request):
        return MenuItem.objects.exclude(pk=1)
admin.site.register(MenuItem, MenuItemAdmin)

#class PageBlockAdmin(ADMIN):
#    list_display = ('__unicode__','page','content_object','is_visible',)
#    list_filter = ('is_visible','page','content_type')
#    related_lookup_fields = {
#        'generic': [['content_type', 'object_id'],],
#    }
#    #form = PageBlockForm
#admin.site.register(PageBlock, PageBlockAdmin)

class FormBlockAdmin(ADMIN):
    list_display = ('slug','form','page','view','url')
    list_filter = ('page','form')
    exclude_fields = ('url',)
    form = FormBlockForm

admin.site.register(FormBlock,FormBlockAdmin)

class PageTemplateAdmin(ADMIN):
    list_display = ('page','slug','template_path')
    prepopulated_fields = {'slug':('page',)}
admin.site.register(PageTemplate,PageTemplateAdmin)

class PageVarAdmin(ADMIN):
    list_display = ('page','context_name','content_type','object_id','object')
    list_filter = ('page',)
admin.site.register(PageVar,PageVarAdmin)


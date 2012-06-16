# -*- coding: utf-8 -*-

from django.contrib import admin
from Kraggne.forms import MenuItemForm, FormBlockForm
from Kraggne.models import MenuItem, PageBlock, FormBlock
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


#class ItemPageInline(admin.TabularInline):
#    model = ItemPage
#    extra = 1
#    form = ItemPageForm


############################################################
class MenuItemAdmin(ADMIN):
    list_display = ('name','slug','order','view','url','parent','level','is_visible','cms_page','__IsAccessible__')
    list_filter = ('is_visible','cms_page')
    prepopulated_fields = {'slug':('name',)}
    form = MenuItemForm
    #inlines = [ItemPageInline,SubMenuItemInline]
    #inlines = [SubMenuItemInline]

    def queryset(self, request):
        return MenuItem.objects.exclude(pk=1)
admin.site.register(MenuItem, MenuItemAdmin)

class PageBlockAdmin(ADMIN):
    list_display = ('__unicode__','page','content_object','is_visible',)
    list_filter = ('is_visible','page','content_type')
    related_lookup_fields = {
        'generic': [['content_type', 'object_id'],],
    }
    #form = PageBlockForm
admin.site.register(PageBlock, PageBlockAdmin)

class FormBlockAdmin(ADMIN):
    list_display = ('slug','form','page')
    list_filter = ('page','form')
    form = FormBlockForm

admin.site.register(FormBlock,FormBlockAdmin)

# -*- coding: utf-8 -*-

from django.contrib import admin
from Kraggne.forms import MenuItemForm
from Kraggne.models import MenuItem, PageBlock

#################### INLINES ################################
class SubMenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1
    form = MenuItemForm
    prepopulated_fields = {'slug':('name',)}


#class ItemPageInline(admin.TabularInline):
#    model = ItemPage
#    extra = 1
#    form = ItemPageForm


############################################################
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name','slug','order','view','url','parent','level','is_visible','cms_page','__IsAccessible__')
    list_filter = ('is_visible','cms_page')
    prepopulated_fields = {'slug':('name',)}
    form = MenuItemForm
    #inlines = [ItemPageInline,SubMenuItemInline]
    inlines = [SubMenuItemInline]

    def queryset(self, request):
        return MenuItem.objects.exclude(pk=1)
admin.site.register(MenuItem, MenuItemAdmin)

class PageBlockAdmin(admin.ModelAdmin):
    list_display = ('__unicode__','page','content_object','slug','is_visible',)
    list_filter = ('is_visible','page')
    #form = PageBlockForm
admin.site.register(PageBlock, PageBlockAdmin)

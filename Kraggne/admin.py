# -*- coding: utf-8 -*-

from django.contrib import admin
from Kraggne.forms import MenuItemForm
from Kraggne.models import MenuItem

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
    list_display = ('name','slug','order','view','url','parent','is_visible','cms_page','__IsAccessible__')
    list_filter = ('is_visible','cms_page')
    prepopulated_fields = {'slug':('name',)}
    form = MenuItemForm
    #inlines = [ItemPageInline,SubMenuItemInline]
    inlines = [SubMenuItemInline]

    def queryset(self, request):
        return MenuItem.objects.exclude(pk=1)
admin.site.register(MenuItem, MenuItemAdmin)

#class ItemPageAdmin(admin.ModelAdmin):
#    list_display = ('__unicode__','parent','rank','content_type','slug','is_visible',)
#    list_filter = ('is_visible','parent')
#    form = ItemPageForm
#admin.site.register(ItemPage, ItemPageAdmin)

from mptt.admin import MPTTModelAdmin
from django.contrib import admin

from Kraggne.model import MenuItem

class MenuItemAdmin(MPTTModelAdmin):
    model = MenuItem

admin.site.register(MenuItem,MenuItemAdmin)

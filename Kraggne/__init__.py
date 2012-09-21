from django.conf import settings

settings.INSTALLED_APPS = (
    'Kraggne.contrib.contentblocks',
    'Kraggne.contrib.flatblocks',
    'Kraggne.contrib.gblocks',) + settings.INSTALLED_APPS

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

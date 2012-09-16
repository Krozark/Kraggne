from django.db import models
from django.utils.translation import ugettext_lazy as _


class Title(models.Model):
    title = models.CharField(_('title'), max_length=255, blank=False)

    def __unicode__(self):
        return "(TitleBlock) %s" % self.title


class Text(models.Model):
    text = models.TextField(_('text'), blank=False)

    def __unicode__(self):
        return "(TextBlock) %s..." % self.text[:20]


class Image(models.Model):
    image = models.ImageField(_('image'), upload_to='gblocks/', blank=False)

    def __unicode__(self):
        return "(ImageBlock) %s" % self.image


class ImageAndLink(models.Model):
    image = models.ImageField(_('image'), upload_to='gblocks/', blank=False)
    link  = models.CharField(_('link'), max_length=255, blank=False)

    def __unicode__(self):
        return "(ImageLinkBlock) %s" % self.image


class TitleAndFile(models.Model):
    title = models.CharField(_('title'), max_length=255, blank=False)
    file = models.FileField(_('file'), upload_to='gblocks/', blank=False)

    def __unicode__(self):
        return "(TitleAndFileBlock) %s" % self.title


class TitleTextAndFile(models.Model):
    title = models.CharField(_('title'), max_length=255, blank=False)
    text = models.TextField(_('text'), blank=False)
    file = models.FileField(_('file'), upload_to='gblocks/', blank=False)

    def __unicode__(self):
        return "(TitleTextAndFileBlock) %s" % self.title


class TitleAndText(models.Model):
    title = models.CharField(_('title'), max_length=255, blank=False)
    text = models.TextField(_('text'), blank=False)

    def __unicode__(self):
        return "(TitleAndTextBlock) %s" % self.title


class TitleTextAndImage(models.Model):
    title = models.CharField(_('title'), max_length=255, blank=False)
    text = models.TextField(_('text'), blank=False)
    image = models.ImageField(_('image'), upload_to='gblocks/', blank=False)

    def __unicode__(self):
        return "(TitleTextAndImageBlock) %s" % self.title


class TitleLinkAndImage(models.Model):
    title = models.CharField(_('title'), max_length=255, blank=False)
    link  = models.CharField(_('link'), max_length=255, blank=False)
    image = models.ImageField(_('image'), upload_to='gblocks/', blank=False)

    def __unicode__(self):
        return "(TitleLinkAndImageBlock) %s" % self.title


class TitleLinkTextAndImage(models.Model):
    title = models.CharField(_('title'), max_length=255, blank=False)
    link  = models.CharField(_('link'), max_length=255, blank=False)
    text = models.TextField(_('text'), blank=False)
    image = models.ImageField(_('image'), upload_to='gblocks/', blank=False)

    def __unicode__(self):
        return "(TitleLinkTextAndImageBlock) %s" % self.title

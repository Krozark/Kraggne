from django.db import models
from django.utils.translation import ugettext_lazy as _
from Kraggne.contrib.gblocks.utils import file_cleanup
from django.db.models.signals import post_delete

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
post_delete.connect(file_cleanup, sender=Image, dispatch_uid="Image.file_cleanup")


class ImageAndLink(models.Model):
    image = models.ImageField(_('image'), upload_to='gblocks/', blank=False)
    link  = models.CharField(_('link'), max_length=255, blank=False)

    def __unicode__(self):
        return "(ImageLinkBlock) %s" % self.image
post_delete.connect(file_cleanup, sender=ImageAndLink, dispatch_uid="ImageAndLink.file_cleanup")


class TitleAndFile(models.Model):
    title = models.CharField(_('title'), max_length=255, blank=False)
    file = models.FileField(_('file'), upload_to='gblocks/', blank=False)

    def __unicode__(self):
        return "(TitleAndFileBlock) %s" % self.title
post_delete.connect(file_cleanup, sender=TitleAndFile, dispatch_uid="TitleAndFile.file_cleanup")


class TitleTextAndFile(models.Model):
    title = models.CharField(_('title'), max_length=255, blank=False)
    text = models.TextField(_('text'), blank=False)
    file = models.FileField(_('file'), upload_to='gblocks/', blank=False)

    def __unicode__(self):
        return "(TitleTextAndFileBlock) %s" % self.title
post_delete.connect(file_cleanup, sender=TitleTextAndFile, dispatch_uid="TitleTextAndFile.file_cleanup")


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
post_delete.connect(file_cleanup, sender=TitleTextAndImage, dispatch_uid="TitleTextAndImage.file_cleanup")


class TitleLinkAndImage(models.Model):
    title = models.CharField(_('title'), max_length=255, blank=False)
    link  = models.CharField(_('link'), max_length=255, blank=False)
    image = models.ImageField(_('image'), upload_to='gblocks/', blank=False)

    def __unicode__(self):
        return "(TitleLinkAndImageBlock) %s" % self.title
post_delete.connect(file_cleanup, sender=TitleLinkAndImage, dispatch_uid="TitleLinkAndImage.file_cleanup")


class TitleLinkTextAndImage(models.Model):
    title = models.CharField(_('title'), max_length=255, blank=False)
    link  = models.CharField(_('link'), max_length=255, blank=False)
    text = models.TextField(_('text'), blank=False)
    image = models.ImageField(_('image'), upload_to='gblocks/', blank=False)

    def __unicode__(self):
        return "(TitleLinkTextAndImageBlock) %s" % self.title
post_delete.connect(file_cleanup, sender=TitleLinkTextAndImage, dispatch_uid="TitleLinkTextAndImage.file_cleanup")

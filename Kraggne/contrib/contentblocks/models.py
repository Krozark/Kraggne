from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from Kraggne.models import MenuItem
#from django.core import serializers
#from Kraggne.contrib.flatblocks.fields import JSONField
from Kraggne.contrib.flatblocks.utils import GetUnknowObjectContent

class PageObject(models.Model):
    content_type = models.ForeignKey(ContentType, limit_choices_to ={'app_label':"flatblocks"})
    object_id = models.PositiveIntegerField(_('object id'))
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    order = models.PositiveIntegerField("order",default=0)

    def __unicode__(self):
        return u'%s' % self.content_object

    #def display(self,context,template_path=None):
    #    return GetUnknowObjectContent(self,context,template_path)

    class Meta:
        ordering = ('order',)



class PageContaineur(models.Model):
    page = models.ForeignKey(MenuItem,blank=True,null=True,default=None)
    hextra_class = models.CharField(_('Hextra css class'),max_length=255,null=True,blank=True,default=None)
    content_objects = models.ManyToManyField(PageObject)
    order = models.PositiveIntegerField("order",default=0)

    def __unicode__(self):
        return u'containeur %d for %s' % (self.order, self.page)

    @property
    def object_list(self):
        return self.content_objects.all()

    #def display(self,context,template_path=None):
    #    return GetUnknowObjectContent(self,context,template_path)

    class Meta:
        ordering = ('page','order')

######################### Alter existing model ###############################
setattr(MenuItem,"get_containeurs",lambda self : PageContaineur.objects.filter(page = self))

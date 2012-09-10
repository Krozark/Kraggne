from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from Kraggne.models import MenuItem
#from django.core import serializers
#from Kraggne.contrib.flatblocks.fields import JSONField
#from Kraggne.contrib.flatblocks.utils import GetBlockContent, GetListContent, GetTemplateContent

class PageObject(model.Model):
    content_type = models.ForeignKey(ContentType, limit_choices_to ={'app_label':"flatblocks"})
    object_id = models.PositiveIntegerField(_('object id'))
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    order = models.PositiveIntegerField(label=_("order"),default=0)



class PageContaineur(model.Model):
    page = models.ForeignKey(MenuItem,blank=True,null=True,default=None)
    hextra_class = models.CharField(_('Hextra css class'),max_length=255,null=True,blank=True,default=None)

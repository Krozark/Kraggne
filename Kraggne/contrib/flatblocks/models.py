from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core import serializers
from Kraggne.contrib.flatblocks.fields import JSONField
from Kraggne.contrib.flatblocks.utils import GetBlockContent, GetListContent, GetTemplateContent

### model use to link to any other model item
class GenericFlatblock(models.Model):
    slug = models.SlugField(_('slug'), max_length=255, unique=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    exclude_fields = JSONField(_('fields not display in template'),blank=True,null=True)

    def __unicode__(self):
        return self.slug

    def model(self):
        return self.content_type.model_class()

    @property
    def fields(self):
        if self.exclude_fields:
            fields = [u.name for u in self.model()._meta.fields if u.name not in self.exclude_fields and u.name != "id" ]
        else:
            fields = [u.name for u in self.model()._meta.fields if u.name != "id" ]
        return fields

    def __iter__(self):
        return self.serialize['fields'].items().__iter__()

    @property
    def serialize(self):
        return serializers.serialize("python", (self.content_object,),fields=self.fields)[0]

    def object_serialize(self):
        return self.content_object, self.serialize()

    def Display(self,context,template_path=None):
        return GetBlockContent(self,context,template_path)

#### model use to link any list of object
class GenericFlatblockList(models.Model):
    slug = models.SlugField(_('slug'), max_length=255, unique=True)
    content_type = models.ForeignKey(ContentType)
    exclude_fields = JSONField(_('fields not display in template'),blank=True,null=True)
    query_args = JSONField(_('custom query args'),blank=True,null=True)

    def __unicode__(self):
        return self.slug

    def model(self):
        return self.content_type.model_class()

    def Display(self,context,template_path=None):
        return GetListContent(self,context,template_path)

    @property
    def object_list(self):
        model = self.content_type.model_class()
        if self.query_args:
            return model.objects.filter(**self.query_args)
        return model.objects.all()

    def __iter__(self):
        return self.object_list.__iter__()


    @property
    def fields(self):
        if self.exclude_fields:
            fields = [u.name for u in self.model()._meta.fields if u.name not in self.exclude_fields and u.name != "id" ]
        else:
            fields = [u.name for u in self.model()._meta.fields if u.name != "id" ]
        return fields

    @property
    def serialize(self):
        return serializers.serialize("python", (self.object_list),fields=self.fields)

    def object_list_serialize(self):
        for obj in self.object_list:
            yield obj, serializers.serialize("python", (obj,),fields=self.fields)[0]

#### model use to get template content passing args
class TemplateBlock(models.Model):
    name = models.CharField(_('Name'), max_length=255, null=False,blank=False)
    slug = models.SlugField(_('slug'), max_length=255, unique=True)
    template_path = models.CharField(_('Template Path'), max_length=255, unique=True)

    def __unicode__(self):
        return self.slug

    def Display(self,context,**kwargs):
        return GetTemplateContent(context,self.template_path,**kwargs)


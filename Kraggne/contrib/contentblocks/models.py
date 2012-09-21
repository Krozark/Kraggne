from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from Kraggne.models import MenuItem
from Kraggne.contrib.contentblocks.utils import get_content_choice_models

class PageObject(models.Model):
    content_type = models.ForeignKey(ContentType, limit_choices_to ={'pk__in':get_content_choice_models()})
    object_id = models.PositiveIntegerField(_('object id'))
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return u'%s' % self.content_object

    def app_label(self):
        return self.content_object._meta.app_label.lower()

    def model_label(self):
        return self.content_object._meta.object_name.lower()


class PageContaineur(models.Model):
    slug = models.SlugField(_('slug'), max_length=255, unique=True,null=True,blank=True)
    page = models.ForeignKey(MenuItem,blank=True,null=True,default=None)
    hextra_class = models.CharField(_('Hextra css class'),max_length=255,null=True,blank=True,default=None)
    content_objects = models.ManyToManyField(PageObject,through="ContaineurToObject",blank=True)
    position = models.PositiveIntegerField("position",default=0)

    def __unicode__(self):
        if self.slug:
            return u"%s" % self.slug
        return u'containeur %d for %s' % (self.position, self.page)

    @property
    def object_list(self):
        return self.containeurtoobject_set.all()
        #return self.content_objects.all()

    class Meta:
        ordering = ('page','position')

class ContaineurToObject(models.Model):
    page_object = models.ForeignKey(PageObject)
    page_containeur = models.ForeignKey(PageContaineur)
    position = models.PositiveIntegerField("position",default=0)

    class Meta:
        ordering = ('page_containeur',"position")

########################## on save ###########################################
from django.db.models.signals import post_save#, pre_save
from django.dispatch import receiver

@receiver(post_save, sender=ContaineurToObject)
@receiver(post_save, sender=PageContaineur)
def sortPosition(sender,**kwargs):
    obj = kwargs['instance']
    kwargs = {'position' : obj.position}
    if isinstance(obj,PageContaineur):
        if not obj.page:
            return
        kwargs["page"] = obj.page
    else: #ContaineurToObject
        kwargs["page_containeur"] = obj.page_containeur

    objs = obj.__class__.objects.filter(**kwargs).exclude(pk = obj.pk)
    i= 1
    for o in objs:
        o.position += i
        o.save()
        i +=1
    

######################### Alter existing model ###############################
setattr(MenuItem,"get_containeurs",lambda self : PageContaineur.objects.filter(page = self))

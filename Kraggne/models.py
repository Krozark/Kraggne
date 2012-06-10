from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.contenttypes.models import ContentType

ORDER_CHOICES = 20

class MenuItem(MPTTModel):
    name = models.CharField(_('Item'),max_length=255)
    order = models.PositiveIntegerField(_('Display order'),
            default=0,
            choices=[(x, x) for x in range(0, ORDER_CHOICES)],
            help_text = _("The order of the item in the display nav."))

    slug = models.SlugField(_('Slug'),unique=True,max_length=50)
    parent = TreeForeignKey('self',null=True,blank=True,default=1)

    cms_page = models.BooleanField(_('CMS page'),default=True,
            help_text=_("Rafere to a stadar or a CMS page."))

    view = models.CharField(_('View'),max_length=255
            ,help_text=_("The view of the page you want to link to, as URL name or absolute URL.\nLeave blank to auto create the url by concatenate parent url and slug."),blank=True,null=True)

    is_visible = models.BooleanField(_('Is Visible'),default=True)
    
    #the calculated url
    url = models.CharField(_('Url'),editable=False,max_length=255)

    class Meta:
        ordering = ('lft', 'tree_id')

    class MPTTMeta:
        order_insertion_by = ['order']

    def __IsAccessible__(self):
        if self.is_visible and self.parent != None:
            return self.parent.__IsAccessible__()
        return self.is_visible

    def get_absolute_url(self):
        return self.url

    def __unicode__(self):
        return u'%s' % self.name



#The choices type of the ItemPage
def getchoices():
    CHOICES = []
    for ct in ContentType.objects.filter(app_label="django_generic_flatblock"):
        m = ct.model_class()
        CHOICES.append("%s.%s" % (m.__module__, m.__name__))
    return CHOICES


#class PageItem(models.Model):
#    parent = models.ForeignKey(ItemMenu,null=False,blank=False,default=1,limit_choices_to = {'pk__in':ItemMenu.objects.filter(auto_create_page=True).exclude(pk=1)})
#
#    rank = models.PositiveIntegerField(_('Rank'),default=0,
#            choices=[(x, x) for x in range(0, ORDER_CHOICES)],
#            help_text = _("The rank of the item in the display nav."))
#
#    content_type = models.CharField(_('Model Type'),max_length=255,
#            choices =[(x,x.split('.')[1]) for x in CHOICES],
#            help_text = _("Content Type of this item"))
#
#    slug = models.SlugField(_('Slug'),unique=True,max_length=50,blank=True,
#        help_text= _("If empty, this slug will be generate using the parent slug en rank"))
#    
#    is_visible = models.BooleanField(_('Is Visible'),default=True)
#
#    class Meta:
#        ordering = ('parent__pk',)
#        verbose_name = _("Page content")
#
#    def get_absolute_url(self):
#        return self.parent.url
#
#    def __unicode__(self):
#        return u'%s #%d %s' % (self.parent.name,self.rank,self.content_type)

    


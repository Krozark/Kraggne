from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey


ORDER_CHOICES = 20

class MenuItem(MPTTModel):
    name = models.CharField(_('Item'),max_length=255)
    slug = models.SlugField(_('Slug'),unique=True,max_length=50)


    

    order = models.PositiveIntegerField(_('Display order'),
            default=0,
            choices=[(x, x) for x in range(0, ORDER_CHOICES)],
            help_text = _("The order of the item in the display nav."))

    parent = TreeForeignKey('self',null=True,blank=True,default=1)

    view = models.CharField(_('View'),max_length=255
            ,help_text=_("The view of the page you want to link to, as URL name or absolute URL.\nLeave blank to auto create the url by concatenate parent url and slug."),blank=True,null=True)
    cms_page = models.BooleanField(_('CMS page'),default=False,
            help_text=_("Rafere to a stadar or a CMS page."))
    #the calculated url
    url = models.CharField(_('Url'),editable=False,max_length=255)
    is_visible = models.BooleanField(_('Is Visible in menu'),default=True)

    #template_path = models.CharField(_('Template Path'), max_length=255,null=True,blank=True,
    #                                 help_text=_('Display usign specific template'))

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


from django.db.models.signals import post_save#, pre_save
from django.dispatch import receiver
from Kraggne.utils import MakePattern#,clearCache

# rebuild url of children if it's nedeed to conserve the base url given
@receiver(post_save, sender=MenuItem)
def MenuItemSave(sender,**kwargs):

    from Kraggne import urls as Kraggne_urls
    if hasattr(Kraggne_urls,'urlpatterns'):
        urls = getattr(Kraggne_urls,'urlpatterns')
        urls += MakePattern(kwargs['instance'])

    children = MenuItem.objects.filter(parent=kwargs['instance'],view='',cms_page=True)
    base_url = kwargs['instance'].url
    for child in children:
        url = child.url
        if base_url == "/":
            child.url = "/"+child.slug
        elif base_url[-1] != "/":
            child.url = base_url +"/"+child.slug
        else:
            child.url = base_url +child.slug

        if url != child.url:
            child.save()


from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class PageBlock(models.Model):
    name = models.CharField(_('Item'),max_length=255)
    page = models.ForeignKey(MenuItem,blank=False,null=False,default=None)
    #content
    # TODO with setting
    content_type = models.ForeignKey(ContentType, limit_choices_to ={'app_label':"flatblocks"})
    object_id = models.PositiveIntegerField(_('object id'))
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    #style
    width = models.PositiveIntegerField(_('Width'),null=False,blank=False,default=100)
    height = models.PositiveIntegerField(_('Height'),null=False,blank=False,default=100)
    hextra_class = models.CharField(_('Hextra css class'),max_length=255,null=True,blank=True,default=None)
    is_visible = models.BooleanField(_('Is Visible'),null=False,blank=False,default=True)
    #position
    position_x = models.IntegerField(_('x position'),null=False,blank=False,default=0)
    position_y = models.IntegerField(_('y position'),null=False,blank=False,default=0)
    template_path = models.CharField(_('Template Path'), max_length=255,null=True,blank=True,
                                     help_text=_('Display usign specific template'))

    class Meta:
        ordering = ('page__lft', 'page__tree_id')

    def get_absolute_url(self):
        return self.page.get_absolute_url()

    def __unicode__(self):
        return u'%s %s' % (self.page,self.name)

class FormBlock(models.Model):
    slug = models.SlugField(_('Slug'),unique=True,max_length=50)
    page = models.OneToOneField(MenuItem)
    form = models.CharField(_('Form'),max_length=255)
    view = models.CharField(_('Redirect View'),max_length=255,blank=True,null=True,
                         help_text=_('Redirect url or named view. Leave blank tu use the url of the display page'))
    url = models.CharField(_('Redirect Url'),max_length=255,blank=True,null=True)

    def getFormClass(self):
        form = self.form
        point = form.rfind('.')
        if point != -1:
            app = form[:point]
            klass = form[point+1:]
            form= __import__(app,globals(),locals(),[klass,])
            form=getattr(form,klass)
        else:
            form=__import__(form)
        return form
        

    class Meta:
        ordering = ('page__lft', 'page__tree_id')

    def get_absolute_url(self):
        return self.page.get_absolute_url()

    def __unicode__(self):
        return u'%s %s' % (self.page,self.slug)



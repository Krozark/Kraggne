from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from django.db.models.loading import get_model
from Kraggne.fields import TemplateField, ContextNameValidator
from Kraggne.contrib.flatblocks.fields import JSONField
from Kraggne.parser import get_model_and_url_from_detail,get_model_from_include
import re

ORDER_CHOICES = 20

class MenuItem(MPTTModel):
    name = models.CharField(_('Item'),max_length=255)
    slug = models.SlugField(_('Slug'),unique=True,max_length=50)


    

    order = models.PositiveIntegerField(_('Display order'),
            default=0,
            choices=[(x, x) for x in range(0, ORDER_CHOICES)],
            help_text = _("The order of the item in the display nav."))

    parent = TreeForeignKey('self',null=True,blank=True,default=1)

    cms_page = models.BooleanField(_('CMS page'),default=False,
            help_text=_("Rafere to a stadar or a CMS page."))

    view = models.CharField(_('View'),max_length=255
            ,help_text=_("The view of the page you want to link to, as url-name, absolute URL (/your/path), include(app.model) or detail(\"/your/path/(?P<what_you_want>[something]+)\",app.model).\nLeave blank to auto create the url by concatenate parent url and slug."),blank=True,null=True)
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

    def is_include(self):
        try:
            return self.url.startswith('include(')
        except:
            return False

    def have_to_display(self):
        return self.is_visible and (self.is_include() or self.is_detail())
        
    def get_model_all(self):
        m = self.get_model()
        if not m:
            return []        
        return m.objects.all()

    def is_detail(self):
        try:
            return self.view.startswith('detail(')
        except:
            return False

    def get_model(self):
        if self.is_include():
            return self._get_for_include_model()
        elif self.is_detail():
            return self._get_for_detail_model()
        return None

    def _get_for_include_model(self):
        return get_model_from_include(self.view)

    def _get_for_detail_model(self):
        model,url = get_model_and_url_from_detail(self.view)
        return model

    def get_object_url(self,obj):
        if hasattr(obj,"get_absolute_url"):
            return obj.get_absolute_url()
        try:
            r = re.compile(self.view)
            attr = r.groupindex.keys()[0]
            return re.sub("(\(.*\))",u"%s" % getattr(obj,attr),self.url)
        except:
            return ""


from django.db.models.signals import post_save#, pre_save
from django.dispatch import receiver

# rebuild url of children if it's nedeed to conserve the base url given
@receiver(post_save, sender=MenuItem)
def MenuItemSave(sender,**kwargs):

    from Kraggne import urls as Kraggne_urls
    from Kraggne.utils import MakePattern
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


class PageVar(models.Model):
    page = models.ForeignKey(MenuItem)
    context_name = models.CharField(_('context name'),max_length=20,validators=[ContextNameValidator])
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField(_('object id'),blank=True,null=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    query_args = JSONField(_('custom query args'),blank=True,null=True)

    class Meta:
        unique_together = (("context_name", "page"),)

    def __unicode__(self):
        return "%s" % self.context_name

    def addToContext(self,context):
        self._addObjectListToContext(context)
        self._addObjectToContext(context)

    def _addObjectToContext(self,context):
        context['%s' % self.context_name] = self.object

    def _addObjectListToContext(self,context):
        context['%s_list' % self.context_name] = self.object_list
        
    def _model(self):
        return self.content_type.model_class()

    @property
    def object(self):
        try:
            return self.content_object
        except:
            return None

    @property
    def object_list(self):
        model = self._model()
        if self.query_args:
            return model.objects.filter(**self.query_args)
        return model.objects.all()

    def __iter__(self):
        return self.object_list.__iter__()

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

class PageTemplate(models.Model):
    page = models.OneToOneField(MenuItem)
    template_path = TemplateField(_('Custom Template'),max_length=255,blank=False,null=False)
    slug = models.SlugField(_('Slug'),unique=True,max_length=255)

    class Meta:
        ordering = ('page__lft', 'page__tree_id')

    def get_absolute_url(self):
        return self.page.get_absolute_url()

    def __unicode__(self):
        return u'%s %s' % (self.page,self.template_path)


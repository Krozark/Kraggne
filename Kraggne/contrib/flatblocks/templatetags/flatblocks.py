from django.template import Library, Node
from django.template import TemplateSyntaxError, TemplateDoesNotExist, Variable
from django.template.loader import select_template
from django.conf import settings
from django.db.models.loading import get_model
from django.template.defaultfilters import slugify
from Kraggne.contrib.flatblocks.models import GenericFlatblock, GenericFlatblockList
from Kraggne.contrib.flatblocks.utils import GetBlockContent, GetListContent, GetTemplateContent

register = Library()

def next_bit_for(bits, key, if_none=None):
    try:
        return bits[bits.index(key)+1]
    except ValueError:
        return if_none

def resolve(var, context):
    """Resolves a variable out of context if it's not in quotes"""
    if not var:
        return None
    if var[0] in ('"', "'") and var[-1] == var[0]:
        return var[1:-1]
    else:
        return Variable(var).resolve(context)

class GenericFlatblockBaseNode(Node):

    def __init__(self, slug, modelname=None, template_path=None, variable_name=None, store_in_object=None):
        self.slug = slug
        self.modelname = modelname
        self.template_path = template_path
        self.variable_name = variable_name
        self.store_in_object = store_in_object
    

    def generate_slug(self, slug, context):
        """
        Generates a slug out of a comma-separated string. Automatically resolves
        variables in it. Examples::

        "website","title" -> website_title
        "website",LANGUAGE_CODE -> website_en
        """
        # If the user passed a integer as slug, use it as a primary key in
        # self.get_content_object()
        if not ',' in slug and isinstance(resolve(slug, context), int):
            return resolve(slug, context)
        return slugify('_'.join([str(resolve(i, context)) for i in slug.split(',')]))

    def generate_admin_link(self, related_object, context):
        """
        Generates a link to contrib.admin change view. In Django 1.1 this
        will work automatically using urlresolvers.
        """
        app_label = related_object._meta.app_label
        module_name = related_object._meta.module_name
        # Check if user has change permissions
        if context['request'].user.is_authenticated() and \
           context['request'].user.has_perm('%s.change' % module_name):
            admin_url_prefix = getattr(settings, 'ADMIN_URL_PREFIX', '/admin/')
            return '%s%s/%s/%s/' % (admin_url_prefix, app_label, module_name, related_object.pk)
        else:
            return None


    def resolve_model_for_label(self, modelname, context):
        """resolves a model for a applabel.modelname string"""
        applabel, modellabel = resolve(modelname, context).split(".")
        related_model = get_model(applabel, modellabel)
        return related_model


class GenericFlatblockNode(GenericFlatblockBaseNode):


    def get_content_object(self, related_model, slug):
        # If the user passed a Integer as a slug, assume that we should fetch
        # this specific object
        if isinstance(slug, int):
            try:
                related_object = related_model._default_manager.get(pk=slug)
                return None, related_object
            except related_model.DoesNotExist:
                if settings.TEMPLATE_DEBUG:
                    raise
                related_object = related_model()
                return None, related_object

        # Otherwise, try to generate a new, related object
        try:
            generic_object = GenericFlatblock._default_manager.get(slug=slug)
            related_object = generic_object.content_object
            if related_object is None:
                # The related object must have been deleted. Let's start over.
                generic_object.delete()
                raise GenericFlatblock.DoesNotExist
        except GenericFlatblock.DoesNotExist:
            related_object = related_model._default_manager.create()
            generic_object = GenericFlatblock._default_manager.create(slug=slug, content_object=related_object)
        return generic_object, related_object



    def render(self, context):
        slug = self.generate_slug(self.slug, context)
        related_model = self.resolve_model_for_label(self.modelname, context)

        # Get the generic and related object
        generic_object, related_object = self.get_content_object(related_model, slug)
        admin_url = self.generate_admin_link(related_object, context)

        # if "into" is provided, store the related object into this variable
        if self.store_in_object:
            into_var = resolve(self.store_in_object, context)
            context[into_var] = related_object
            return ''


        content= GetBlockContent(generic_object,context,resolve(self.template_path,context))

        # Set content as variable inside context, if variable_name is given
        if self.variable_name:
            context[resolve(self.variable_name, context)] = content
            return ''
        return content

def do_genericflatblock(parser, token):
    """
    {% gblock "slug" for "appname.modelname" %}
    {% gblock "slug" for "appname.modelname" into "slug_object" %}
    {% gblock "slug" for "appname.modelname" with "templatename.html" %}
    {% gblock "slug" for "appname.modelname" with "templatename.html" as "variable" %}
    """

    bits = token.contents.split()
    args = {
        'slug': next_bit_for(bits, 'gblock'),
        'modelname': next_bit_for(bits, 'for'),
        'template_path': next_bit_for(bits, 'with'),
        'variable_name': next_bit_for(bits, 'as'),
        'store_in_object': next_bit_for(bits, 'into'),
    }
    return GenericFlatblockNode(**args)

register.tag('gblock', do_genericflatblock)
######################################################################
##################### LIST ###########################################
######################################################################


from django.contrib.contenttypes.models import ContentType
class GenericFlatblockListNode(GenericFlatblockBaseNode):


    def get_content_object(self, related_model, slug):

        # If the user passed a Integer as a slug, assume that we should fetch
        # this specific object
        try:
            generic_object = GenericFlatblockList._default_manager.get(slug=slug)
        except GenericFlatblockList.DoesNotExist:
            generic_object = GenericFlatblockList._default_manager.create(slug=slug,content_type=ContentType.objects.get_for_model(related_model))
        return generic_object



    def render(self, context):

        slug = self.generate_slug(self.slug, context)
        related_model = self.resolve_model_for_label(self.modelname, context)

        # Get the generic and related object
        generic_object = self.get_content_object(related_model, slug)

        # if "into" is provided, store the related object into this variable
        if self.store_in_object:
            into_var = resolve(self.store_in_object, context)
            context[into_var] = generic_object
            return ''


        # Resolve the template(s)
        content = GetListContent(generic_object,context,resolve(self.template_path,context))

        # Set content as variable inside context, if variable_name is given
        if self.variable_name:
            context[resolve(self.variable_name, context)] = content
            return ''
        return content

def do_genericflatblocklist(parser, token):
    """
    {% glist "slug" for "appname.modelname" %}
    {% glist "slug" for "appname.modelname" into "slug_object" %}
    {% glist "slug" for "appname.modelname" with "templatename.html" %}
    {% glist "slug" for "appname.modelname" with "templatename.html" as "variable" %}
    """

    bits = token.contents.split()
    args = {
        'slug': next_bit_for(bits, 'glist'),
        'modelname': next_bit_for(bits, 'for'),
        'template_path': next_bit_for(bits, 'with'),
        'variable_name': next_bit_for(bits, 'as'),
        'store_in_object': next_bit_for(bits, 'into'),
    }
    return GenericFlatblockListNode(**args)

register.tag('glist', do_genericflatblocklist)


##############################################################
################ display tag #################################
##############################################################

class DisplayNode(Node):

    def __init__(self, obj, template_path):
        self.obj = obj
        self.template_path = template_path

    def render(self,context):
        return resolve(self.obj,context).Display(context,self.template_path)

def do_display(parser, token):
    """
    {% display obj [with template_path ] %}
    """

    bits = token.contents.split()
    obj = next_bit_for(bits, 'display')
    template = next_bit_for(bits,'with')

    return DisplayNode(obj,template)
register.tag('display', do_display)

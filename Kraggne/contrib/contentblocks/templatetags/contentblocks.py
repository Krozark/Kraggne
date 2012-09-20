from django.template import Library, Node
from django.template import Variable
#from django.template.loader import select_template
from django.conf import settings
from django.template.defaultfilters import slugify
from Kraggne.contrib.flatblocks.utils import GetUnknowObjectContent
from Kraggne.contrib.contentblocks.models import PageContaineur

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


#########################$ containeur #############################

class PageContaineurNode(Node):

    def __init__(self, slug=None,store_in_object = None,template_path=None, variable_name = None):
        self.slug = slug

        self.store_in_object = store_in_object
        self.template_path = template_path
        self.variable_name = variable_name

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

    def get_content_object(self, slug):
        # If the user passed a Integer as a slug, assume that we should fetch
        # this specific object

        if not slug:
            return None

        if isinstance(slug, int):
            try:
                obj,c = PageContaineur.objects.get_or_create(pk=slug)
                if c:
                    obj.slug = "auto-generated-%d" % slug
                    obj.hextra_class = self.hextra_class
                    obj.save()
                return obj
            except PageContaineur.DoesNotExist:
                if settings.TEMPLATE_DEBUG:
                    raise
                return None

        obj, c = PageContaineur.objects.get_or_create(slug=slug)
        #if c:
        #    obj.hextra_class = self.hextra_class
        #    obj.save()
        return obj

    def render(self, context):

        slug = self.generate_slug(self.slug, context)
        obj = self.get_content_object(slug)

        if not obj:
            return ""

        if self.store_in_object:
            into_var = resolve(self.store_in_object, context)
            context[into_var] = obj
            return ''

        content = GetUnknowObjectContent(obj,context,resolve(self.template_path,context))

        # Set content as variable inside context, if variable_name is given
        if self.variable_name:
            context[resolve(self.variable_name, context)] = content
            return ''
        return content


def do_containeur(parser,token):
    """
    create or get a containeur and display  it

    {% containeur "slug" %}
    {% containeur "slug" into "slug_name" %}
    {% containeur "slug" with "template_path" %}
    {% containeur "slug" with "template_path" as "variable_name" %}
    """

    bits = token.contents.split()
    args = {
        'slug': next_bit_for(bits, 'containeur'),
        'store_in_object': next_bit_for(bits, 'into'),
        'template_path': next_bit_for(bits, 'with'),
        'variable_name': next_bit_for(bits, 'as'),
    }
    return PageContaineurNode(**args)
register.tag("containeur",do_containeur)



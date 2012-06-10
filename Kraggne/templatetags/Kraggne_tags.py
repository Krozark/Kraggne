from django.template import Library, Node
from django.template.loader import select_template TemplateSyntaxError, TemplateDoesNotExist, Variable

from Kraggne.models import MenuItem

register = Library()

def next_bit_for(bits, key, if_none=None):
    try:
        return bits[bits.index(key)+1]
    except ValueError:
        return if_none

def resolve(self, var, context):
    """Resolves a variable out of context if it's not in quotes"""
    if var[0] in ('"', "'") and var[-1] == var[0]:
        return var[1:-1]
    else:
        return Variable(var).resolve(context)

def GetMenuBySlug(slug):
    try:
        return MenuItem.objects.get(slug=slug)
    except:
        return None

class breadcumbNode(Node):

    def __init__(self, slug,template_path=None,store_in_object=None,variable_name=None):
        self.slug = slug
        self.template_path = template_path
        self.store_in_object = store_in_object
        self.variable_name = variable_name

    def render(self, context):
        memu = GetMenuBySlug(self.slug)
        if not memu:
            return ''

        breadcrumb = menu.get_ancestors(include_self=True)

        if self.store_in_object:
            context[resolve(self.store_in_object,context)] = breadcrumb
            return ''

        template_paths = []
        if self.template_path:
            template_paths.append(resolve(self.template_path, context))
        template_paths.append('Kraggne/breadcrumb.html')
            
        try:
            t = select_template(template_paths)
        except:
            return ''

        # Set content as variable inside context, if variable_name is given
        if self.variable_name:
            context[resolve(self.variable_name, context)] = breadcrumb
        else:
            context['object_list'] = breadcrumb

        content = t.render(context)
        return content


def do_breadcrumb(parser, token):
    """
    {% breadcrumb "slug" %}
    {% breadcrumb "slug" into "slug_object" %}
    {% breadcrumb "slug" with "templatename.html" %}
    {% breadcrumb "slug" with "templatename.html" as "variable" %}
    """

    def next_bit_for(bits, key, if_none=None):
        try:
            return bits[bits.index(key)+1]
        except ValueError:
            return if_none


    bits = token.contents.split()
    args = {
        'slug': next_bit_for(bits, 'menu_breadcrumb'),
        'store_in_object': next_bit_for(bits, 'into'),
        'template_path': next_bit_for(bits, 'with'),
        'variable_name': next_bit_for(bits, 'as'),
    }
    return breadcumbNode(**args)

register.tag('menu_breadcrumb', do_breadcrumb)



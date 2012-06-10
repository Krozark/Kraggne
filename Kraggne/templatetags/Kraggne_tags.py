# -*- coding: utf-8 -*-

from django.template import Library, Node, TemplateSyntaxError, TemplateDoesNotExist, Variable
from django.template.loader import select_template
from Kraggne.models import MenuItem

register = Library()

################################################################
############## COMMUN FUNCTIONS ################################
################################################################

def next_bit_for(bits, key, if_none=None):
    try:
        res = bits[bits.index(key)+1]
        if res in ('as','for','with','into') or "=" in res:
            return if_none
        return res
    except:
        return if_none

def get_val_for(bits,key,if_none=None,type=bool):
    for u in bits:
        if u.startswith(key+"="):
            res = u.split('=')[1]
            if type == bool:
                return res=='True'
            return type(res)
    return if_none


def resolve(var, context):
    """Resolves a variable out of context if it's not in quotes"""
    if var[0] in ('"', "'") and var[-1] == var[0]:
        return var[1:-1]
    else:
        try : 
            return context[var]
        except:
            return var

def GetMenuBySlug(slug):
    try:
        return MenuItem.objects.get(slug=slug)
    except:
        return None

################################################################
#######################" BREADCRUMB ############################
################################################################

class breadcumbNode(Node):

    def __init__(self, slug=None,template_path=None,store_in_object=None,variable_name=None,include_self=True):
        self.slug = slug
        self.template_path = template_path
        self.store_in_object = store_in_object
        self.variable_name = variable_name
        self.include_self = include_self

    def render(self, context):
        if not self.slug:
            try:
                self.slug = context["page_slug"]
            except:
                return ''

        menu = GetMenuBySlug(resolve(self.slug,context))

        if not menu:
            return ''

        breadcrumb = menu.get_ancestors(include_self=self.include_self).filter(is_visible = True)

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
    {% breadcrumb ["slug"] [include_self=True] %}
    {% breadcrumb ["slug"] into "slug_object" [include_self=True] %}
    {% breadcrumb ["slug"] with "templatename.html" [include_self=True] %}
    {% breadcrumb ["slug"] with "templatename.html" as "variable" [include_self=True] %}
    """

    bits = token.contents.split()
    args = {
        'slug': next_bit_for(bits, 'breadcrumb'),
        'store_in_object': next_bit_for(bits, 'into'),
        'template_path': next_bit_for(bits, 'with'),
        'variable_name': next_bit_for(bits, 'as'),
        'include_self' : get_val_for(bits,'include_self',if_none=True,type=bool)
    }
    return breadcumbNode(**args)

register.tag('breadcrumb', do_breadcrumb)

##################################################################
####################### SHOW MENU ################################
##################################################################

class menuNode(Node):

    def __init__(self, slug,template_path=None,store_in_object=None,variable_name=None,include_self=True):
        self.slug = slug
        self.template_path = template_path
        self.store_in_object = store_in_object
        self.variable_name = variable_name
        self.include_self = include_self

#is_ancestor_of(other, include_self=True)
#get_descendants(include_self=False)
    def render(self, context):
        menu = GetMenuBySlug(resolve(self.slug,context))
        if not menu:
            return ''

        tree = menu.get_descendants(include_self=self.include_self)

        if self.store_in_object:
            context[resolve(self.store_in_object,context)] = tree
            return ''

        template_paths = []
        if self.template_path:
            template_paths.append(resolve(self.template_path, context))
        template_paths.append('Kraggne/menu.html')
            
        try:
            t = select_template(template_paths)
        except:
            return ''

        # Set content as variable inside context, if variable_name is given
        if self.variable_name:
            context[resolve(self.variable_name, context)] = tree
        else:
            context['object_list'] = tree

        content = t.render(context)
        return content


        return ''

def do_menu(parser, token):
    """
    {% menu "slug" [include_self=True] %}
    {% menu "slug" into "slug_object" [include_self=True] %}
    {% menu "slug" with "templatename.html" [include_self=True] %}
    {% menu "slug" with "templatename.html" as "variable" [include_self=True] %}
    """

    bits = token.contents.split()
    args = {
        'slug': next_bit_for(bits, 'menu'),
        'store_in_object': next_bit_for(bits, 'into'),
        'template_path': next_bit_for(bits, 'with'),
        'variable_name': next_bit_for(bits, 'as'),
        'include_self' : get_val_for(bits,'include_self',if_none=True,type=bool)
    }
    return menuNode(**args)

register.tag('menu', do_menu)



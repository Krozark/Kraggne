# -*- coding: utf-8 -*-

from django.template import Library, Node, TemplateSyntaxError, TemplateDoesNotExist, Variable
from django.template.loader import select_template
import operator

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
        try:
            return Variable(var).resolve(context)
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
                menu = context["page"]
            except:
                return ''
        else:
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

    def __init__(self, slug,template_path=None,store_in_object=None,variable_name=None,include_self=True,fulltree=True):
        self.slug = slug
        self.template_path = template_path
        self.store_in_object = store_in_object
        self.variable_name = variable_name
        self.include_self = include_self
        self.fulltree = fulltree

    def render(self, context):

        if not self.slug:
            try:
                menu = context["page"]
            except:
                return ''
        else:
            menu = GetMenuBySlug(resolve(self.slug,context))

        if not menu:
            return ''


        if self.fulltree:
            tree = menu.get_descendants(include_self=self.include_self).filter(is_visible=True)
        else:
            tree = menu.get_children()
        context['root'] = menu

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
    {% menu ["slug"] [include_self=True fulltree=True] %}
    {% menu ["slug"] into "slug_object" [include_self=True fulltree=True] %}
    {% menu ["slug"] with "templatename.html" [include_self=True fulltree=True] %}
    {% menu ["slug"] with "templatename.html" as "variable" [include_self=True fulltree=True] %}
    """

    bits = token.contents.split()
    args = {
        'slug': next_bit_for(bits, 'menu'),
        'store_in_object': next_bit_for(bits, 'into'),
        'template_path': next_bit_for(bits, 'with'),
        'variable_name': next_bit_for(bits, 'as'),
        'include_self' : get_val_for(bits,'include_self',if_none=True,type=bool),
        'fulltree' : get_val_for(bits,'fulltree',if_none=True,type=bool),
    }
    return menuNode(**args)

register.tag('menu', do_menu)

####################################################################
###################### compare #####################################
####################################################################

class lastNode(Node):

    def __init__(self,op,var,dest):
        self.op = op
        self.var=var
        self.dest=dest

    def render(self, context):
        var = Variable(self.var).resolve(context)
        counter = Variable('forloop.counter0').resolve(context)
        res = False

        if counter == 0:
            context['last_value'] = var
            context[self.dest] = False
            return''

        if context.has_key('last_value'):
            res = getattr(operator,self.op)((context['last_value']),var)
        context['last_value'] = var
        context[self.dest] = res
        return ''


        
def do_last(parser, token):
    """
    {% last == obj2 var %}
    {% last != obj2 var %}
    {% last <= obj2 var %}
    {% last < obj2 var %}
    {% last >= obj2 var %}
    {% last > obj2 var %}
    """

    bits = token.contents.split()
    if bits.__len__() != 4:
        return ''
    op = bits[1]
    if op == "==":
        op = "eq"
    elif op == "!=":
        op = "ne"
    elif op == "<=":
        op = "le"
    elif op == "<":
        op = "lt"
    elif op == ">=":
        op = "ge"
    elif op == ">":
        op = "gt"
    else:
        return ''

    return lastNode(op,bits[2],bits[3])

register.tag('last', do_last)

##########################################################################
######################### UTILS TAGS #####################################
##########################################################################
#class GetMenuNode(Node):
#
#    def __init__(self,store_in_object=None):
#        self.store_in_object = store_in_object or 'page_itemmenu'
#
#    def render(self, context):
#        try:
#            slug = context["page_slug"]
#            context[resolve(self.store_in_object,context)] = MenuItem.objects.get(slug=slug)
#        except:
#            pass
#        return ''
#
#def do_getmenu(parser, token):
#    """
#    {% getmenu [into "slug_object"] %}
#    """
#
#    bits = token.contents.split()
#    args = {
#        'store_in_object': next_bit_for(bits, 'into'),
#    }
#    return GetMenuNode(**args)
#
#register.tag('getmenu', do_getmenu)


@register.filter
def ancestor(arg,val):
    print arg,val
    return arg.is_ancestor_of(val,include_self=True)

@register.filter
def descendant(arg,val):
    print arg,val
    return arg.is_descendant_of(val,include_self=True)


@register.filter
def range(arg,value ):
    arg = arg or 0
    value = value or 0
    res = xrange(arg,value)
   # if (arg > value):
   #     res = res.__reversed__()
    return res

@register.filter
def sub(arg, value ):
    return arg-value



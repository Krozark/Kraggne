# -*- coding: utf-8 -*-

from django.template import Library, Node, TemplateSyntaxError, TemplateDoesNotExist, Variable
from django.template.loader import select_template
import operator

from Kraggne.models import MenuItem
from django.db.models import Q
from django import forms

register = Library()
def push_context(context,indices = ["generic_object","object","generic_object_list"]):
    save = {}
    for i in indices:
        save[i] = context.get(i)
    return save

def pop_context(context,save):
    for i in save.keys():
        context[i] = save[i]
    return context
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

        breadcrumb = menu.get_ancestors(include_self=self.include_self).filter(Q(is_visible = True) | Q(pk=menu.pk))

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
        save = {}
        if self.variable_name:
            save = push_context(context,resolve(self.variable_name, context))
            context[resolve(self.variable_name, context)] = breadcrumb
        else:
            save = push_context(context,["object_list",])
            context['object_list'] = breadcrumb

        content = t.render(context)
        context = pop_context(context,save)
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

    def __init__(self, slug,template_path=None,store_in_object=None,variable_name=None,include_self=True,level_min=0,level_nb=0,context = {}):
        self.slug = slug
        self.template_path = template_path
        self.store_in_object = store_in_object
        self.variable_name = variable_name
        self.include_self = include_self
        self.level_min = level_min
        self.level_nb = level_nb
        self.context = context

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

        context.update(self.context)
        
        if self.level_min > 0:
            tree = menu.get_descendants(include_self=self.include_self).filter(is_visible=True,level__gte=menu.level+self.level_min)
        elif self.level_min < 0:
            tmp = menu
            menu = menu.get_ancestors(include_self=True).filter(level__gte=menu.level+self.level_min-1)[0]
            tree = menu.get_descendants(include_self=False).filter(is_visible=True)
            if self.include_self == False:
                tree=tree.exclude(pk__in=tmp.get_descendants(include_self=True))
        else:
            tree = menu.get_descendants(include_self=self.include_self).filter(is_visible=True)

        if self.level_nb > 0:
            tree = tree.filter(level__lte = menu.level+self.level_nb)

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
        save = {}
        if self.variable_name:
            save = push_context(context,resolve(self.variable_name, context))
            context[resolve(self.variable_name, context)] = tree
        else:
            save = push_context(context,["object_list",])
            context['object_list'] = tree

        content = t.render(context)
        context = pop_context(context,save)
        return content


        return ''

def do_menu(parser, token):
    """
    {% menu ["slug"] [include_self=True level_min=0 level_nb=0] %}
    {% menu ["slug"] into "slug_object" [include_self=True level_min=0 level_nb=0] %}
    {% menu ["slug"] with "templatename.html" [include_self=True level_min=0 level_nb=0] %}
    {% menu ["slug"] with "templatename.html" as "variable" [include_self=True level_min=0 level_nb=0] %}
    the level_min arg is relative to the menu pass in arg
    level_min must be <= 0 for a good result. if >0, the result can change, and is not guarantie
    """

    bits = token.contents.split()
    args = {
        'slug': next_bit_for(bits, 'menu'),
        'store_in_object': next_bit_for(bits, 'into'),
        'template_path': next_bit_for(bits, 'with'),
        'variable_name': next_bit_for(bits, 'as'),
        'include_self' : get_val_for(bits,'include_self',if_none=True,type=bool),
        'level_min' : get_val_for(bits,'level_min',if_none=0,type=int),
        'level_nb' : get_val_for(bits,'level_nb',if_none=0,type=int),
        'context' : {'MENU_CLASS' : 'menu',}
    }
    return menuNode(**args)

register.tag('menu', do_menu)

####################################################################
###################### Sous menu ###################################
####################################################################

def do_sousmenu(parser, token):
    """
    {% sousmenu ["slug"] [include_self=False level_min=0 level_nb=1] %}
    {% sousmenu ["slug"] into "slug_object" [include_self=False level_min=0 level_nb=1] %}
    {% sousmenu ["slug"] with "templatename.html" [include_self=False level_min=0 level_nb=1] %}
    {% sousmenu ["slug"] with "templatename.html" as "variable" [include_self=False level_min=0 level_nb=1] %}
    the level_min arg is relative to the menu pass in arg
    level_min must be <= 0 for a good result. if >0, the result can change, and is not guarantie
    """
    bits = token.contents.split()
    args = {
        'slug': next_bit_for(bits, 'menu'),
        'store_in_object': next_bit_for(bits, 'into'),
        'template_path': next_bit_for(bits, 'with'),
        'variable_name': next_bit_for(bits, 'as'),
        'include_self' : get_val_for(bits,'include_self',if_none=False,type=bool),
        'level_min' : get_val_for(bits,'level_min',if_none=0,type=int),
        'level_nb' : get_val_for(bits,'level_nb',if_none=1,type=int),
        'context' : {'MENU_CLASS' : 'sousmenu',}
    }
    return menuNode(**args)

register.tag('sousmenu', do_sousmenu)

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
class GetMenuNode(Node):

    def render(self, context):
        try:
            menu = context["page"]
            if isinstance(menu,str):
                menu = GetMenuBySlug(menu)
                context["page"] = menu
        except:
            pass
        return ''

def do_getmenu(parser, token):
    """
    {% getmenu %}
    """
    return GetMenuNode()

register.tag('getmenu', do_getmenu)


@register.filter
def ancestor(arg,val):
    if not arg or not val:
        return False
    return arg.is_ancestor_of(val,include_self=True)

@register.filter
def descendant(arg,val):
    if not arg or not val:
        return False
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

@register.filter
def startswith(arg, val):
    return arg.startswith(val)

@register.filter
def get_object_url(menu,obj):
    return menu.get_object_url(obj)

##############################################################
################ display tag #################################
##############################################################
from django.template.loader import select_template, get_template, find_template

class TryDisplayNode(Node):

    def __init__(self, obj, template_path):
        self.obj = obj
        self.template_path = template_path

    def render(self,context):
        o = resolve(self.obj,context)
        if not o:
            return ""
        if hasattr(o,"display"):
            return o.display(context,self.template_path)

        template_paths = [self.template_path,]
        if hasattr(o, '_meta'):
            template_paths.append('%s/%s/%s.html' % (o._meta.app_label.lower(),o._meta.object_name.lower(),'object'))

        try:
            t = select_template(template_paths)
        except Exception,e:
            return 'no template find to display %s.%s model (or not valid).\n Exception : %s' % ( o._meta.app_label,o._meta.object_name,e )
        save = push_context(context,["object",])
        context["object"] = o
        res = t.render(context)
        context = pop_context(context,save)
        return res


def do_try_display(parser, token):
    """
    {% try_display obj [with template_path ] %}
    """

    bits = token.contents.split()
    obj = next_bit_for(bits, 'try_display')
    template = next_bit_for(bits,'with')

    return TryDisplayNode(obj,template)
register.tag('try_display', do_try_display)


class DisplayFormNode(Node):

    def __init__(self, obj, template_path):
        self.obj = obj
        self.template_path = template_path

    def render(self,context):
        o = resolve(self.obj,context)
        if not o:
            return ""
        if hasattr(o,"display"):
            return o.display(context,self.template_path)

        template_paths = [self.template_path,]
        if issubclass(o.__class__,forms.ModelForm):
            try:
                template_paths.append('%s/%s/%s.html' % (o._meta.model._meta.app_label.lower(),o._meta.model._meta.object_name.lower(),'form'))
            except:
                pass

        template_paths.append('Kraggne/form.html')

        try:
            t = select_template(template_paths)
        except Exception,e:
            return 'no template find to display the form (or not valid).\n Exception : %s' % e 

        save = push_context(context,["form",])
        context["form"] = o
        res = t.render(context)
        context = pop_context(context,save)
        return res

@register.tag
def displayform(parser,token):
    """
    {% displayform form [with template_path ] %}
    """
    bits = token.contents.split()
    obj = next_bit_for(bits, 'displayform')
    template = next_bit_for(bits,'with')

    return DisplayFormNode(obj,template)


################################### pagination ################################
class PaginationNode(Node):
    NUM_PAGE_CENTRE = 2

    def link (self,num,active=False,get=""):
        if active:
            return "&nbsp;<a class='active' href='?page="+str(num)+get+"'>"+str(num)+"</a>"
        else:
            return "&nbsp;<a class='link' href='?page="+str(num)+get+"'>"+str(num)+"</a>"

    def render(self,context):
        page_obj = resolve("page_obj",context)
        if not page_obj:
            return ""

        res =""
        get = ""
        request = context["request"]
        for u in request.GET.keys():
            if u != "page":
                get+="&%s=%s" % (u,request.GET[u])

        current = page_obj.number
        m = page_obj.paginator.num_pages
        
        if m >1:
            if current >1:
                res+='<a href="?page='+str(current-1)+'" class="prev">&laquo;</a>'

                res += self.link(1,get=get)

                if (current - self.NUM_PAGE_CENTRE > 2):
                    res += "&nbsp;..."

                i = 1
                c = ""
                while ( i <= self.NUM_PAGE_CENTRE and current -i >1):
                    c =self.link(current-i,get=get)+ c
                    i+=1
                res +=c

            res+=self.link(current,active=True,get=get)

            if current < m:
                #on met un lien vers les pages autour (apres)
                i = 1
                while ( i <= self.NUM_PAGE_CENTRE and current + i < m):
                    res+=self.link(current+i,get=get)
                    i+=1
                    #on met les liens vers les ...
                if ( current+ self.NUM_PAGE_CENTRE +1< m):
                    res+="&nbsp;..."
                res+=self.link(m,get=get)
                res+='<a href="?page='+str(current+1)+get+'" class="next">&raquo;</a>'
        return res


def do_pagination(parser,token):
    return PaginationNode()
register.tag("pagination",do_pagination)



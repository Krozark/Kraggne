from django.template.loader import select_template, get_template, find_template

def GetTemplatesPath(appname,modelname,type,template_path=None):
    template_paths = []
    if template_path:
        template_paths.append(template_path)
    template_paths.append('%s/%s/%s.html' % (appname.lower(),modelname.lower(),type))
    return template_paths

def GetBlockContent(obj,context,template_path=None):
    template_paths = GetTemplatesPath(obj.content_type.app_label,obj.content_type.model,'object',template_path)
    template_paths.append("flatblocks/object.html")
    try:
        t = select_template(template_paths)
    except:
        return ''
    context["generic_object"] = obj
    context["object"] = obj.content_object
    return t.render(context)

def GetUnknowObjectContent(obj,context,template_path=None):
    template_paths = GetTemplatesPath(obj._meta.app_label,obj._meta.object_name,'object',template_path)
    #template_paths.append("flatblocks/unknow_object.html")
    try:
        t = select_template(template_paths)
    except Exception,e:
        return 'no template find to display %s.%s model (or not valid).\n Exception : %s' % ( obj._meta.app_label,obj._meta.object_name,e )
    context["object"] = obj
    return t.render(context)


def GetListContent(obj,context,template_path=None):
    template_paths = GetTemplatesPath(obj.content_type.app_label,obj.content_type.model,'object_list',template_path)
    simple_obj_template_path = GetTemplatesPath(obj.content_type.app_label,obj.content_type.model,'object',template_path)[0]
    try:
        t = find_template(simple_obj_template_path)
        print "found"
        template_paths.append("flatblocks/object_list_by_object.html")
        context["object_file_to_include"] = simple_obj_template_path
    except Exception,e:
        print e
        print simple_obj_template_path
        pass

    template_paths.append("flatblocks/object_list.html")
    try:
        t = select_template(template_paths)
    except:
        return ''
    context['generic_object_list'] = obj
    return t.render(context)

def GetTemplateContent(context,template_path,**kwargs):
    try:
        t = get_template(template_path)
        print t
    except:
        return ''
    context.update(kwargs)
    return t.render(context)


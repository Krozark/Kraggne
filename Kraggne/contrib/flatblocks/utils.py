from django.template.loader import select_template

def GetTemplatesPath(appname,modelname,type,template_path=None):
    template_paths = []
    if template_path:
        template_paths.append(template_path)
    template_paths.append('%s/%s/%s.html' % (appname,modelname,type))
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

def GetUnknowObjectContent(obj,context,template_paths=None):
    template_paths = GetTemplatesPath(obj._meta.app_label,obj._meta.object_name,'object',template_path)
    template_paths.append("flatblocks/unknow_object.html")
    try:
        t = select_template(template_paths)
    except:
        return 'no template find to display %s.%s model.' % ( obj._meta.app_label,obj._meta.object_name )
    context["object"] = obj
    return t.render(context)


def GetListContent(obj,context,template_path=None):
    template_paths = GetTemplatesPath(obj.content_type.app_label,obj.content_type.model,'object_list',template_path)
    template_paths.append("flatblocks/object_list.html")
    try:
        t = select_template(template_paths)
    except:
        return ''
    context['generic_object_list'] = obj
    return t.render(context)

def GetTemplateContent(context,template_path,**kwargs):
    try:
        t = select_template(template_paths)
    except:
        return ''
    context.update(kwargs)
    return t.render(context)

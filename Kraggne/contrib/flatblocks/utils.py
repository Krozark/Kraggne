from django.template.loader import select_template, get_template, find_template

def push_context(context,indices = ["generic_object","object","generic_object_list"]):
    save = {}
    for i in indices:
        save[i] = context.get(i)
    return save

def pop_context(context,save):
    for i in save.keys():
        context[i] = save[i]
    return context

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

    save = push_context(context,["generic_object","object"])
    context["generic_object"] = obj
    context["object"] = obj.content_object
    res = t.render(context)
    context = pop_context(context,save)

    return res

def GetUnknowObjectContent(obj,context,template_path=None):
    template_paths = GetTemplatesPath(obj._meta.app_label,obj._meta.object_name,'object',template_path)
    #template_paths.append("flatblocks/unknow_object.html")
    try:
        t = select_template(template_paths)
    except Exception,e:
        return 'no template find to display %s.%s model (or not valid).\n Exception : %s' % ( obj._meta.app_label,obj._meta.object_name,e )

    save = push_context(context,["object",])
    context["object"] = obj
    res = t.render(context)
    context = pop_context(context,save)

    return res


def GetListContent(obj,context,template_path=None):
    template_paths = GetTemplatesPath(obj.content_type.app_label,obj.content_type.model,'object_list',template_path)
    simple_obj_template_path = GetTemplatesPath(obj.content_type.app_label,obj.content_type.model,'object',template_path)[0]
    try:
        t = find_template(simple_obj_template_path)
        template_paths.append("flatblocks/object_list_by_object.html")
        context["object_file_to_include"] = simple_obj_template_path
    except Exception,e:
        pass

    template_paths.append("flatblocks/object_list.html")
    try:
        t = select_template(template_paths)
    except:
        return ''

    save = push_context(context,["generic_object_list",])
    context['generic_object_list'] = obj
    res = t.render(context)
    context = pop_context(context,save)

    return res

def GetTemplateContent(context,template_path,**kwargs):
    try:
        t = get_template(template_path)
    except:
        return ''

    save = push_context(context,**kwargs)
    context.update(kwargs)
    res = t.render(context)
    context = pop_context(context,save)

    return res


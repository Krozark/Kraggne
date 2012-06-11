from django.template.loader import select_template

def GetTemplatesPath(modelname,type,template_path=None):
    template_paths = []
    if template_path:
        template_paths.append(template_path)
    var = modelname.lower().split(".")
    template_paths.append('%s/%s/%s.html' % (var[0],var[1],type))
    return template_paths

def GetBlockContent(obj,context,template_path=None):
    template_paths = GetTemplatesPath('django_generic_flatblocks.GenericFlatblock','object',template_path)
    template_paths.append("django_generic_flatblocks/object.html")
    try:
        t = select_template(template_paths)
    except:
        return ''
    context["generic_object"] = obj
    return t.render(context)


def GetListContent(obj,context,template_path=None):
    template_paths = GetTemplatesPath('django_generic_flatblocks.GenericFlatblockList','object_list',template_path)
    template_paths.append("django_generic_flatblocks/object_list.html")
    try:
        t = select_template(template_paths)
    except:
        return ''
    context['generic_object_list'] = obj
    return t.render(context)

def GetTemplateContent(obj,template_path=None):
    pass

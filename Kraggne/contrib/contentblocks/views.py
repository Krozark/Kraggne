# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.utils import simplejson as json
from django.views.generic import TemplateView, FormView
from django.db.models.loading import get_model
from django.core.urlresolvers import reverse
from django.template import Context

from Kraggne.contrib.contentblocks.utils import get_content_choice_models,model_to_modelform
from Kraggne.contrib.contentblocks.models import *
from Kraggne.contrib.flatblocks.utils import GetUnknowObjectContent


def error(data=None):
    if not data:
        return HttpResponse('{"st":"error","data"="error"}',content_type='application/json')
    else :
        return HttpResponse('{"st":"error","data"="%s"}' % data ,content_type='application/json')


class AjaxRecieverView(FormView):

    def to_hidden(self,name):
        return '<input type="hidden" value="'+self.request.POST[name]+'" name="'+name+'">'
    
    def get(self,request, *args, **kwargs):
        return error("get not accept")

    def post(self,request, *args, **kwargs):
        if not request.user.is_anonymous() and request.user.is_staff:
            status = request.POST["st"]

            if not status :
                return error("wat i'v to do?")

            if status =="add-req":
                #add new item
                choices = get_content_choice_models()
                return HttpResponse(
                    json.dumps({
                        "st" : "ok",
                        "choices" : [ (x.pk,x.__unicode__()) for x in choices],
                    }),
                    content_type='application/json')
            elif status == "get-form":
                model = get_content_choice_models().filter(pk=request.POST["contenttype_pk"])
                if not model:
                    return error("no model found")
                model = model[0].model_class()
                form = model_to_modelform(model)()
                return HttpResponse(
                    json.dumps({
                        "st" : "ok",
                        "form" : form.as_p()
                    }),
                    content_type='application/json')

            elif status == "add-content":
                containeur = PageContaineur.objects.filter(pk=int(request.POST["obj_id"]))
                if not containeur:
                    return error("where i've to put the object?")
                containeur = containeur[0]

                receive_object = get_content_choice_models().filter(pk=request.POST["contenttype_pk"])
                if not receive_object:
                    return error("no model found with this type")
                receive_object = receive_object[0].model_class()
                form = model_to_modelform(receive_object)(request.POST,request.FILES)

                status = "ok"
                hextra_data = None

                if form.is_valid():
                    obj = form.save()
                    p = PageObject(content_object=obj)
                    c2obj = ContaineurToObject(page_object=p,page_containeur=containeur)
                    hextra_data = {
                        "html" : GetUnknowObjectContent(c2obj,Context(self.get_context_data(**kwargs))),
                        "type" : "add",
                        "containeur-id" : containeur.pk,
                    }

                else :
                    status = "error"
                    hextra_data = {
                        "hiddens" : self.to_hidden("app_name")+\
                        self.to_hidden("module_name")+\
                        self.to_hidden("obj_id")+\
                        self.to_hidden("st")+\
                        self.to_hidden("contenttype_pk")+\
                        form.as_p(),
                        "type" : "form",
                    }

                status = json.dumps({
                    "st" : status,
                    "data" : hextra_data
                }),
                return HttpResponse("""<script language="javascript" type="text/javascript">
                                    window.top.window.formUploadCallback(%s);
                                    </script>""" % status)

            model = get_model(request.POST["app_name"],request.POST["module_name"])

            if not model:
                return error("no model")
            obj = model.objects.filter(pk=int(request.POST["obj_id"]))
            if not obj:
                return error("no object found")
            obj = obj[0]

            print model
            print obj

            return HttpResponse("ok")
        return error

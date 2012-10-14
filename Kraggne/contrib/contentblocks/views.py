# -*- coding: utf-8 -*-
import os

from django.http import HttpResponse
from django.utils import simplejson as json
from django.views.generic import TemplateView, FormView
from django.db.models.loading import get_model
from django.core.urlresolvers import reverse
from django.core.files.base import ContentFile
from django.template import Context
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

from Kraggne.contrib.contentblocks.utils import get_content_choice_models,model_to_modelform
from Kraggne.contrib.contentblocks.models import *
from Kraggne.contrib.flatblocks.utils import GetUnknowObjectContent
from Kraggne.contrib.contentblocks.conf.settings import IMG_EXT_CHOICE

from Kraggne.contrib.gblocks.models import TitleAndFile, Image

def error(data=None):
    if not data:
        return HttpResponse('{"st":"error","data":"error"}',content_type='application/json')
    else :
        return HttpResponse('{"st":"error","data":"%s"}' % data ,content_type='application/json')


class AjaxRecieverView(FormView):

    def to_hidden(self,name):
        return '<input type="hidden" value="'+self.request.POST[name]+'" name="'+name+'">'

    def GetUnknowObjectContent(self,obj,**kwargs):
        return GetUnknowObjectContent(obj,
                                      Context(self.get_context_data(
                                          user=self.request.user,
                                          MEDIA_URL=settings.MEDIA_URL,
                                          STATIC_URL=settings.STATIC_URL,
                                          request=self.request,
                                          **kwargs)
                                      ))
    
    def get(self,request, *args, **kwargs):
        return error("get not accept")

    def post(self,request, *args, **kwargs):
        if not request.user.is_anonymous() and request.user.is_staff:
            try:
                status = request.POST["st"]
            except:
                status = request.GET["st"]


            if not status :
                return error("what i've to do?")

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
                    obj = form.save(commit=False)
                    kwargs = {}
                    for field in obj._meta.fields:
                        if field.name != "id":
                          kwargs[field.name] = getattr(obj,field.name)
                          o = receive_object.objects.filter(**kwargs)[:1]
                    if o:
                        obj = o[0]
                    else:
                        #TODO verifier que l'objet existe pas déja
                        obj.save()
                    #if isinstance(obj,PageContaineur):
                    p = PageObject(content_object=obj)
                    p.save()
                    c2obj = ContaineurToObject(page_object=p,page_containeur=containeur)
                    c2obj.save()
                    hextra_data = {
                        "html" : self.GetUnknowObjectContent(c2obj,**kwargs),
                        "type" : "add",
                        "containeur_id" : containeur.pk,
                    }

                else :
                    status = "error"
                    hextra_data = {
                        "form" : self.to_hidden("app_name")+\
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
            elif status == "del-content":
                if request.POST["app_name"] != "contentblocks" or request.POST["module_name"] != "containeurtoobject":
                    return error("impossible to delete this objet")

                obj = ContaineurToObject.objects.filter(pk=int(request.POST["obj_id"]))
                if not obj:
                    return error("no object found")
                obj = obj[0]
                page_obj = obj.page_object
                obj.delete()
                if page_obj.containeurtoobject_set.count() == 0:
                    obj = page_obj.content_object
                    page_obj.delete()
                    if PageObject.objects.filter(content_type=ContentType.objects.get_for_model(obj),object_id=obj.pk).count() == 0:
                        obj.delete()
                return HttpResponse('{"st":"ok","data":"Objet suprimé"}',content_type='application/json')

            elif status == "obj-maj":
                if request.POST["app_name"] != "contentblocks" or request.POST["module_name"] != "containeurtoobject":
                    return error("impossible to delete this objet")

                obj = ContaineurToObject.objects.filter(pk=int(request.POST["obj_id"]))
                containeur = PageContaineur.objects.filter(pk=int(request.POST["parent_id"]))
                if not obj or not containeur:
                    return error("no object found")
                obj = obj[0]
                containeur = containeur[0]

                obj.page_containeur = containeur
                obj.position = int(request.POST["obj_position"])
                obj.save()
                return HttpResponse(u'{"st":"ok","data":"Objet bougé"}',content_type='application/json')

            elif status == "upload-file":
                uploaded = request.read
                filesize = int(uploaded.im_self.META["CONTENT_LENGTH"])
                filename = uploaded.im_self.META["HTTP_X_FILE_NAME"]

                containeur_id = int(self.request.GET["obj_id"])

                content = ContentFile(request.read(filesize))
                basename, ext = os.path.splitext(str(filename))

                obj = None
                if ext.lower() in IMG_EXT_CHOICE :
                    obj = self.create_gblocks_file(Image,"image",filename,content,containeur_id)
                else:
                    obj = self.create_gblocks_file(TitleAndFile,"file",filename,content,containeur_id,title=basename)

                if not obj:
                    return error("mauvaises donnee recues")

                content = json.dumps({
                    "st" : "ok",
                    "data" : {
                        "html" : self.GetUnknowObjectContent(obj,**kwargs),
                        "containeur_id" : containeur_id
                    }
                })

                return HttpResponse(content,content_type='application/json')
        return error

    def create_gblocks_file(self,model,file_name_attr,path,content,containeur_id,title=None):
        containeur = PageContaineur.objects.filter(pk=containeur_id)
        if not containeur:
            return None
        containeur = containeur[0]

        obj = model()
        f = getattr(obj,file_name_attr)
        f.save(path,content,save=True)
        if title:
            obj.title = title
        obj.save()

        p = PageObject(content_object=obj)
        p.save()

        c2obj = ContaineurToObject(page_object=p,page_containeur=containeur)
        c2obj.save()

        return c2obj

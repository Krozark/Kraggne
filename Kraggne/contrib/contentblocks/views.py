# -*- coding: utf-8 -*-

from django.views.generic import TemplateView, FormView
from django.http import HttpResponse
from Kraggne.contrib.contentblocks.utils import get_content_choice_models,model_to_modelform
from django.db.models.loading import get_model
from django.utils import simplejson as json
from django.core.urlresolvers import reverse

error = HttpResponse('{"st":"error"}',content_type='application/json')

class AjaxRecieverView(FormView):
    
    def get(self, *args, **kwargs):
        return error

    def post(self, *args, **kwargs):
        if not self.request.user.is_anonymous() and self.request.user.is_staff:
            status = self.request.POST["st"]

            if not status :
                return error

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
                model = get_content_choice_models().filter(pk=self.request.POST["contenttype_pk"])
                if not model:
                    return error
                model = model[0].model_class()
                form = model_to_modelform(model)()
                return HttpResponse(
                    json.dumps({
                        "st" : "ok",
                        "form" : form.as_p()
                    }),
                    content_type='application/json')
            elif status == "add-content":
                print self.request.POST
                print self.request.FILES
                status = "ok"
                return HttpResponse("""<script language="javascript" type="text/javascript">
                                    window.top.window.formUploadCallback("%s");
                                    </script>""" % status)


            model = get_model(self.request.POST["app_name"],self.request.POST["module_name"])
            #form = model_to_modelform(model)()

            if not model:
                return error
            obj = model.objects.filter(pk=int(self.request.POST["obj_id"]))
            if not obj:
                return error
            obj = obj[0]


            print model
            print obj

            return HttpResponse("ok")
        return error

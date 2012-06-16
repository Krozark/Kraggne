# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from Kraggne.contrib.flatblocks.models import GenericFlatblockList, GenericFlatblock, TemplateBlock
import json

class GenericFlatblockForm(ModelForm):

    class Meta:
        model = GenericFlatblock

    def clean_exclude_fields(self):
        fields = json.loads(self.cleaned_data["exclude_fields"])
        if fields:
            model = self.cleaned_data["content_type"].model_class()
            for u in fields:
                if u not in model._meta.get_all_field_names():
                    raise forms.ValidationError(_("%s is not in the related model, choces are : %s" % (u,model._meta.get_all_field_names())))
        return fields

    def save(self, commit=True):
        block = super(GenericFlatblockForm, self).save(commit=False)
        block.exclude_fields = self.cleaned_data["exclude_fields"]

        if commit:
            block.save() 

        return block

class GenericFlatblockListForm(ModelForm):

    class Meta:
        model = GenericFlatblockList

    def clean_exclude_fields(self):
        fields = json.loads(self.cleaned_data["exclude_fields"])
        if fields:
            model = self.cleaned_data["content_type"].model_class()
            for u in fields:
                if u not in model._meta.get_all_field_names():
                    raise forms.ValidationError(_("%s is not in the related model, choces are : %s" % (u,model._meta.get_all_field_names())))
        return fields

    def clean_query_args(self):
        args = json.loads(self.cleaned_data["query_args"])
        if args:
            model = self.cleaned_data["content_type"].model_class()
            try :
                model.objects.filter(**args)
            except Exception,e:
                raise forms.ValidationError("%s" % e)

        return args
        

    def save(self, commit=True):
        block = super(GenericFlatblockListForm, self).save(commit=False)
        block.exclude_fields = self.cleaned_data["exclude_fields"]
        block.query_args = self.cleaned_data["query_args"]

        if commit:
            block.save() 

        return block

from django.template.loader import select_template
class TempateBlockForm(ModelForm):

    class Meta:
        model  = TemplateBlock

    def clean_template_path(self):
        tpl = self.cleaned_data['template_path']
        try:
            select_template((tpl,))
        except Exception,e:
            raise forms.ValidationError("Template %s not found" % e)

        return tpl

    def save(self, commit=True):
        block = super(TempateBlockForm, self).save(commit=False)
        block.template_path = self.cleaned_data['template_path']

        if commit:
            block.save() 

        return block


# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from django_generic_flatblocks.models import GenericFlatblockList, GenericFlatblock
import json

class GenericFlatblockForm(ModelForm):

    class Meta:
        model = GenericFlatblock

    def clean_exclude_fields(self):
        fields = json.loads(self.cleaned_data["exclude_fields"])
        if fields:
            model = self.cleaned_data["content_type"].model_class()
            print model
            for u in fields:
                if u not in model._meta.get_all_field_names():
                    raise forms.ValidationError(_("%s is not in the related model, choces are : %s" % (u,model._meta.get_all_field_names())))
        return fields

    def save(self, commit=True):
        block = super(GenericFlatblockForm, self).save(commit=False)
        block.exclude_fields = self.cleaned_data["exclude_fields"]

        if commit:
            block.save() 
            pass
        return block

class GenericFlatblockListForm(ModelForm):

    class Meta:
        model = GenericFlatblockList

    def clean_exclude_fields(self):
        fields = json.loads(self.cleaned_data["exclude_fields"])
        if fields:
            model = self.cleaned_data["content_type"].model_class()
            print model
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
            pass
        return block


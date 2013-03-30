from django import forms
from django.forms import ValidationError

from django.core.validators import URLValidator
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
import re
from Kraggne.utils import MakePattern, clean_url

from Kraggne.models import MenuItem, FormBlock

class MenuItemForm(forms.ModelForm):

    class Meta:
        model = MenuItem

    def clean_view(self):
        link = self.cleaned_data['view'] or ''
        # It could be a fully-qualified URL -- try that first b/c reverse()
        # chokes on "http://"

        if any([link.startswith(s) for s in ('http://', 'https://')]):
            URLValidator()(link)
            self.url = link
            return self.cleaned_data['view']

        auto = self.cleaned_data['cms_page']

        if not auto:
            if link:
               link,self.url = clean_url(link,include=True,detail=True)
               return link
            raise ValidationError(_('Please supply a valid URL or URL name.'))

        else: #auto
            if link:
                link,self.url = clean_url(link,include=True,detail=True,lis=True,existe=False)
                return link
                #try:
                #    re.compile(link)
                #    self.url = link
                #    return link
                #except:
                #    raise forms.ValidationError(_("%s is not a valide Regex." % link))
                #elif link[0] != "/":
                #    self.url = "/"+link
                #else:
                #    self.url = link
                #return link
        
        parent = self.cleaned_data['parent']
        if parent:
            p_url = parent.url
            if '#' in p_url:
                p_url = p_url[:p_url.find('#')]

            if p_url == "/":
                self.url = "/"+self.cleaned_data['slug'] 
            elif p_url[-1] != "/":
                self.url = p_url +"/"+self.cleaned_data['slug']
            else:
                self.url = p_url +self.cleaned_data['slug'] 
        else:
            self.url = "/"+self.cleaned_data['slug']
        return ''

    def clean(self):
        super(MenuItemForm, self).clean()

        #if 'is_visible' in self.cleaned_data and \
        #  self.cleaned_data['is_visible'] and \
        #  'view' in self.cleaned_data and \
        #  self.cleaned_data['view'].startswith('^'):
        #    raise forms.ValidationError(_('Menu items with regular expression URLs must be disabled.'))
        return self.cleaned_data

    def save(self, commit=True):
        item = super(MenuItemForm, self).save(commit=False)
        item.view = self.cleaned_data['view']
        item.url = self.url
        if item.view:
            if not 'include(' in item.view and not 'detail(' in item.view and not 'list(' in item.view and not any([item.view.startswith(s) for s in ('http://', 'https://')]):
                if re.search('[^\d/\w\-:_#? ]',item.view):
                    item.is_visible = False
        
        ##try to register the new url
        #if hasattr(Kraggne_urls,'urlpatterns'):
        #    urls = getattr(Kraggne_urls,'urlpatterns')
        #    urls += MakePattern(item)

        if commit:
            item.save() 
        return item

class FormBlockForm(forms.ModelForm):
    class Meta:
        model = FormBlock


    def clean_view(self):
        view = self.cleaned_data['view']
        self.url = view
        if view:
            view,self.url = clean_url(view)
        if view and view[-1] != "/":
            self.url+="/"
        return view

    def clean_form(self):
        form = self.cleaned_data['form']
        try:
            point = form.rfind('.')
            if point != -1:
                app = form[:point]
                klass = form[point+1:]
                f= __import__(app,globals(),locals(),[klass,])
                f=getattr(f,klass)
            else:
                f=__import__(form)

            try:
                f.is_valid
            except :#TypeError:
                raise forms.ValidationError(_("%s is not a form" % form))
        except :#ImportError:
            raise forms.ValidationError(_("%s could not be found" % form))
        return form
    
    def save_m2m(self):
        pass

    def save(self,commit=True):
        form = super(FormBlockForm,self).save()
        form.view = self.cleaned_data['view']
        form.form = self.cleaned_data['form']
        form.url = self.url

        if commit:
            form.save(commit=True)

        return form

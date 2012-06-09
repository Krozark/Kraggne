from django import forms
from django.core.urlresolvers import reverse, NoReverseMatch
from django.core.validators import URLValidator
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django.test.client import Client
import re

from Kraggne import urls as Kraggne_urls
from Kraggne.utils import MakePattern

from Kraggne.models import MenuItem


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
                if link[0] == "/": #a defined URL
                    c = Client()
                    try:
                        resp = c.get(link)
                        if resp.status_code == 404:
                            raise forms.ValidationError(_(u'%s is not a local URL (does not exist)' % link))
                        self.url = link
                        return link
                    except:
                        raise forms.ValidationError(_(u'%s is not a local URL (not a valid URL)' % link))

                elif link[0] != '^' : # Not a regex or site-root-relative absolute path
                    try: # named URL or view
                        self.url = reverse(link)
                        return link
                    except NoReverseMatch:
                        raise forms.ValidationError(_('No view find to display the page, and cms_page is disable.\nPlease create a view named %s, or enable cms_page.' % link))
                elif link[0] == '^': #regex
                    raise forms.ValidationError(_('Regex are not suported with not CMS items. Please use named url insted'))
            raise forms.ValidationError(_('Please supply a valid URL or URL name.'))

        else: #auto
            if link:
                if link[0] == '^': #regex
                    try:
                        re.compile(link)
                        return link
                    except:
                        raise forms.ValidationError(_("%s is not a valide Regex." % link))
                elif link[0] != "/":
                    self.url = "/"+link
                else:
                    self.url = link
                return link
        
        parent = self.cleaned_data['parent']
        if parent:
            if parent.url == "/":
                self.url = "/"+self.cleaned_data['slug'] 
            elif parent.url[-1] != "/":
                self.url = parent.url +"/"+self.cleaned_data['slug']
            else:
                self.url = parent.url +self.cleaned_data['slug'] 
        else:
            self.url = "/"+self.cleaned_data['slug']
        return self.cleaned_data['slug']

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
        item.url = self.url
        
        #try to register the new url
        if hasattr(Kraggne_urls,'urlpatterns'):
            urls = getattr(Kraggne_urls,'urlpatterns')
            urls += MakePattern(item)

        if commit:
            item.save() 
            pass
        return item



#class InlineMenuItemForm(forms.ModelForm):
#    #queryset=ItemMenu.objects.all()
#
#    class Meta:
#        model = ItemMenu
#        fields = ('parent', 'name', 'slug', 'rank', 'is_visible')
#
#class ItemPageForm(forms.ModelForm):
#    
#    class Meta:
#        model = ItemPage
#
#    def clean_parent(self):
#        parent = self.cleaned_data['parent']
#        if not parent.auto_create_page:
#            raise forms.ValidationError(_("generic content are not allow to parent that don't have 'auto_create_page' activated"))
#        return parent
#
#    def clean_slug(self):
#        slug = self.cleaned_data['slug']
#        if slug != "":
#            return slugify(slug)
#
#        parent = self.cleaned_data['parent']
#        rank = self.cleaned_data['rank']
#
#        return slugify("%s-%d" % (parent.slug,rank))
#        

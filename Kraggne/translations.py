from modeltranslation.translator import translator, TranslationOptions
from Kraggne.models import *

class MenuItemTrans(TranslationOptions):
    fields = ('name',)
translator.register(MenuItem,MenuItemTrans)

class PageBlockTrans(TranslationOptions):
    fields = ('name',)
translator.register(PageBlock,PageBlockTrans)

class FormBlockTrans(TranslationOptions):
    fields = ()
translator.register(FormBlock,FormBlockTrans)

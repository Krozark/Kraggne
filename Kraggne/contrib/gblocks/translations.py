# -*- coding: utf-8 -*-

from modeltranslation.translator import translator, TranslationOptions
from Kraggne.contrib.gblocks.models import *


class TitleOptions(TranslationOptions):
    fields = ('title',)
translator.register(Title, TitleOptions)


class TextOptions(TranslationOptions):
    fields = ('text',)
translator.register(Text, TextOptions)


class ImageAndLinkOptions(TranslationOptions):
    fields = ('link', 'image')
translator.register(ImageAndLink, ImageAndLinkOptions)


class TitleAndFileOptions(TranslationOptions):
    fields = ('title', 'image')
translator.register(TitleAndFile, TitleAndFileOptions)


class TitleTextAndFileOptions(TranslationOptions):
    fields = ('title', 'text', 'file')
translator.register(TitleTextAndFile, TitleTextAndFileOptions)


class TitleAndTextOptions(TranslationOptions):
    fields = ('title', 'text',)
translator.register(TitleAndText, TitleAndTextOptions)


class TitleTextAndImageOptions(TranslationOptions):
    fields = ('title', 'text', 'image')
translator.register(TitleTextAndImage, TitleTextAndImageOptions)


class TitleLinkAndImageOptions(TranslationOptions):
    fields = ('title', 'link', 'image')
translator.register(TitleLinkAndImage, TitleLinkAndImageOptions)


class TitleLinkTextAndImageOptions(TranslationOptions):
    fields = ('title', 'link', 'text', 'image')
translator.register(TitleLinkTextAndImage, TitleLinkTextAndImageOptions)

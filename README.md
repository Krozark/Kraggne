video
======

    http://www.dailymotion.com/video/xtnmu2_kraggne-tuto-1_tech

Kraggne
=======

Un projet de cms django, mais n,empèche pas de tout codder "à la main" et prpose meme des fonctions pour aller plus vite.


Instalation:
-----------
     
    in your INSTALLED_APPS add :
        'mptt'
        'Kraggne'

    in your urls.py add :
        (r'',            include('Kraggne.urls')),

    the first time you run syncdb, initial data must be created:
        syncdb
        loaddata data/main_menu.json


Menu Gestion:
------------
    {% load Kraggne_tags %}

    {% menu ["slug"] [include_self=True level_min=0 level_nb=0] %}
    {% menu ["slug"] into "slug_object" [include_self=True level_min=0 level_nb=0] %}
    {% menu ["slug"] with "templatename.html" [include_self=True level_min=0 level_nb=0] %}
    {% menu ["slug"] with "templatename.html" as "variable" [include_self=True level_min=0 level_nb=0] %}
    
    {% sousmenu ["slug"] [include_self=False level_min=0 level_nb=1] %}
    {% sousmenu ["slug"] into "slug_object" [include_self=False level_min=0 level_nb=1] %}
    {% sousmenu ["slug"] with "templatename.html" [include_self=False level_min=0 level_nb=1] %}
    {% sousmenu ["slug"] with "templatename.html" as "variable" [include_self=False level_min=0 level_nb=1] %}
    
    {% getmenu %}
    look if context['page'] is a string, it will try to get the menuitem with this slug, and put it in context['page']
    
     warning:
     ---------
     
    I recomend you, to use this tag in all your template that use a other Kraggne tag,
    and what are display using a custom (def) view or that not extend Kraggne.views.GenericViewContextMixinSlug (and not a CSM page).
    Put it in the top of the page, before any Kraggne Tag/filter to disable possible TypeErrors. 



Breadcrumb:
----------

    {% load Kraggne_tags %}

    {% breadcrumb ["slug"] [include_self=True] %}
    {% breadcrumb ["slug"] into "slug_object" [include_self=True] %}
    {% breadcrumb ["slug"] with "templatename.html" [include_self=True] %}
    {% breadcrumb ["slug"] with "templatename.html" as "variable" [include_self=True] %}


Custom views:
------------

     You can esily use your own view insted of CMS. But you have to extend Kraggne.views.GenericViewContextMixinSlug
     to provide Menu/breadcrumb functionement, and add a
     slug= 'my-page-slug' that is your current page slug (set in the admin)

Models
======


MenuItem:
--------

    This object is the base, it permit you to add new url and/or creat new pages.

    All  Cms MenuItem create a new named url as:
    name = kraggne-[item-slug]
    url = item.url
    view = Kraggne.view.GenericView (or GenericFormView if a form is link to the item or GenericDetailView (see after))

    in the form it can be url,named-url,detail('url',app.model),include(app.model)
    note : 
        detail create a Use the GenericDetailView if 'is_visible' is True' and use the 'get_absolute_url()' (or the url regex  if not existing)
        it use also the <pk> or <slug> attribut (in url and object) to get it. If want want to get the object with a other way you can, but you have to add a get_object_from_url(**kwargs) methode where kwargs is the url parameters

    template = Kraggne/Generic[Form/Detail]Page.html (depend of the view) by default. You can customise it creating a templatevar link to the item (but you have to reboot the django server [i'm not able to destroy the cache], sorry :/ )

    context :
        context["page"] = current menuItem
        for all pageVars link with the item:
            context[var.context_name] = generic_object (if a pk is set)
            context[var.context_name+'_list'] = generic_object model.all() (or .filter(**kwargs) where 
            kwargs is the custom query args)
            the object_list is set all the time. the object, only if the object_id is set (and existe)

        context["form"] = The form classe associate to the view (for GenericFormView only)
        context["object"] = The object to display (GenericDetailView only)

        all the template extends the base.html template
        all the content is put in the block: {% block page.body %}{% endblock %}. don't forget to add it in your base.html

            

Blocks of content (contrib.gblocks)
===================================

    this app is juste some usefull models that can be use to display different content:
    Title,Text,Image,ImageAndLink,TitleAndFile,TitleTextAndFile,TitleAndText,TitleTextAndImage,TitleLinkAndImage,TitleLinkTextAndImage
    this models can be cominate with the folowing app


Generic Block (contrib.flatblocks): 
=============

Block 
------

    {% load  generic_flatblocks %}

    {% gblock "test-block" for "gblocks.Text"  %}
    {% gblock "test-block" for "gblocks.Text" into object  %}
    {% gblock "test-block" for "gblocks.Text" with tempate_path %}
    {% gblock "test-block" for "gblocks.Text" with template_path as varable_name %}

    you can also display a block using:
    {% display your_block_var %}


    the default templates used are (in order):
        [template_path]
        [app]/[model]/object.html (were app and model retere to object._meta.app_label.lower() and object._meta.model.lower() )
        flatblocks/object.html (generic, display all the items, but surly not as you want)



List
-----

    {% load  generic_flatblocks %}

    {% glist "test-list" for "gblocks.Text"  %}
    {% glist "test-list" for "gblocks.Text" into object  %}
    {% glist "test-list" for "gblocks.Text" with tempate_path %}
    {% glist "test-list" for "gblocks.Text" with template_path as varable_name %}

    you can also display a list using:
    {% display your_list_var %}

    the default templates used are (in order):
        [template_path]
        [app]/[model]/object_list.html (were app and model retere to object._meta.app_label.lower() and object._meta.model.lower() )
        flatblocks/object_list_by_object.html (generic that use the custom object.html ([app]/[model]/object.html) if it existe )
        flatblocks/object_list.html (generic, display all the items, but surly not as you want)


Template
--------

    This model can be use only with a block (put it inside).
    This model refer to a existing template, and include it in your page

    Exemple:
        "blocks/menu.inc.html" to include the main menu
        "blocks/sub-menu.inc.html" to include the curent sub-menu


content Blocks (contrib.contentblocks)
======================================

    this app is the one who display the CMS.

    all the model can be display with the {% display object %} tag (even yours) [refer to Generic/Block] to see the templates uses

Containeur:
-----------
    This model is just a placeHolder. if it's link to a specifique page, it'll be display in it automaticly ( if you use one of the GenericPageView(s)).
    you can order them using the position field.
    Page refer to the page where it will be display
    Hextra css are som optional css class (to cutom easily your interface)
    slug is use with the containeur tags

    tags:

    create or get a containeur and display  it

    {% containeur "slug" [css_class=None] [page=None] %}
    {% containeur "slug" into "slug_name" [css_class=None] [page=None] %}
    {% containeur "slug" with "template_path" [css_class=None] [page=None] %}
    {% containeur "slug" with "template_path" as "variable_name" [css_class=None] [page=None] %}

    {% load contentblocks %}
    {% containeur "footer" css_class="footer" %} to create a new container

    html display:

    <div class="contentblocks containeur [hextra_class]" id="[slug or pk if not existe]">
        {% for object in object.object_list %}
        {% display object %} (see containeurToObject to see the HTML)
        {% endfor %}
    </div>

Containeur To Object:
--------------------
    
    it simply a lnk between a PageObject and a containeur where it will be display. Nomaly you don't have to use it manualy
    it have a position field to choose the position of the lnked pageObject in the Containeur (use Dragg&drop connecting with a admin account to change it easily) 

    html:

    <div class="contentblocks object">
        {% display object.page_object %} (see PageObject to see css)
    </div>


page Object:
-----------
    
    it's juste a genericforeignkey to a object (restric choice with CONTENTBLOCKS_CONTENT_CHOICE_MODELS in your settings, see CONTENTBLOCKS_CONTENT_CHOICE_MODELS.conf.settings to view default)

    html:

    <div class="contentblocks-blocks [object model name]">
        {% display object.content_object %} (your template is put here (or default))
    </div>


Exemple:
-------


    {% load Kraggne_tags generic_flatblocks %}
    {% getmenu %}

    <h1>{{ page.title}}</h1>

    {% menu level_min=-1 level_nb=3 include_self=False %}

    {% breadcrumb %}

    {% gblocks "text" for "gblocks.Text" %}
    {% glist "users-list" for "auth.user" %}

    {% containeur "footer" css_class="footer" %}

    see Kraggne/template/base.html to see more



css:
====

    if you want to use css (or custom it):
        cd {Kragge dir}/Kraggne/static/Kraggne
    sass --watsh sass:css

    in your html:
    <link href="{{STATIC_URL}}Kraggne/css/all.css" rel="stylesheet">



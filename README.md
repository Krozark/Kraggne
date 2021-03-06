video
======

    http://www.dailymotion.com/video/xtnmu2_kraggne-tuto-1_tech
    http://www.dailymotion.com/video/xtq7m6_kraggne-dragg-drop-tuto-2_tech#.UOQvkfkWWC0

Kraggne
=======

Un projet de cms django, mais n'empèche pas de tout coder "à la main" et prpose des fonctions pour aller plus vite.


Instalation:
-----------
     
    in your INSTALLED_APPS add :
        'mptt',
        'Kraggne.contrib.contentblocks',
        'Kraggne.contrib.flatblocks',
        'Kraggne.contrib.gblocks',
        'Kraggne',



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
     
    I recomend you, to use this tag in all your template that use a other Kraggne tag (for exemple in your base.html),
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

     You can easily use your own view insted of CMS. But you have to extend Kraggne.views.GenericViewContextMixin to provide Menu/breadcrumb functionement, and add a slug= 'my-page-slug' that is your current page slug (set in the admin)

     if you use a custom class view that extend Kraggne.views.GenericViewContextMixin (or GenericView/GenericFormView/GenericDetailView/GenericListView/GenericListFormView) add the slug attr (slug refer to the MenuItem.slug link) to get the correct menuItem in context.

     If you creat a model and you want to display a list of it (with list(url,app.model)[see MenuItem] or with a view extend GenericListView), you can add it a "paginate_by" attr to your model if you want to paginate it (default = 10) set None to disable pagination.
     you can use {% pagination %} tag to display the pagination block ({% load Kraggne_tags %}).

Models
======


MenuItem:
--------

    This object is the base, it permit you to add new url and/or creat new pages.

    All  Cms MenuItem create a new named url as:
    name = kraggne-[item-slug]
    url = item.url
    view = Kraggne.view.GenericView (or GenericFormView if a form is link to the item or GenericDetailView (see after))

    in the form it can be url,named-url,detail('url',app.model),include(app.model),list('url',app.model)
    note : 
        detail create a Use the GenericDetailView if 'is_visible' is True' and use the 'get_absolute_url()' (or the url regex  if not existing)
        it use also the <pk> or <slug> attribut (in url and object) to get it. If want want to get the object with a other way you can, but you have to add a get_object_from_url(**kwargs) methode where kwargs is the url parameters

    template = Kraggne/Generic[List/Detail/FormList]Page.html (depend of the view) by default. You can customise it creating a templatevar link to the item (but you have to reboot the django server [i'm not able to destroy the cache], sorry :/ ) or by creat a [app]/[model]/[object/list/detail/formlist].html template. In the case of FormView, [app]/[model]/[list/formlist] are enable

    context :
        context["page"] = current menuItem
        for all pageVars link with the item:
            context[var.context_name] = generic_object (if a pk is set)
            context[var.context_name+'_list'] = generic_object model.all() (or .filter(**kwargs) where 
            kwargs is the custom query args)
            the object_list is set all the time. the object, only if the object_id is set (and existe)

        context["form"] = The form classe associate to the view (for Generic[List]FormView only)
        context["object"] = The object to display (GenericDetailView only)
        context["object_list"] = The list of object to display (Generic[Form]ListView only)

        all the template extends the base.html template
        all the content is put in the block: {% block page.body %}{% endblock %}. don't forget to add it in your base.html


    List,Detail,Form,ListForm and DetailForm are actualy possible to auto create just usign the admin.


    Generic[List/Detail]FormView can be use with a django ModelForm or a BasForm.
    The success_url can be set, or will be calculated as following:
        with ModelForm:
            get_absolute_url of the new object if existe
        else:
            use the url set in the for link with the page if existe, else use the page url
        in all case #form is add at the end of the url (set in the template, so you can delete it by customize the template)

    if use with a ModelForm,the form.save have this param : comit=True[,request=request]. The request param is a optional, if you want to add som attr manualy (object.user for exemple)

    You can custom the display html of all form:
    Kraggne/form.html

    For a specifique form :
    [module]/forms/[Form class name].html

    For a model form:
    [app]/[model]/form.html
            

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
        [app]/[model]/object.html (were app and model refere to object._meta.app_label.lower() and object._meta.model.lower() )
        flatblocks/object.html (generic, display all the items, but surly not as you want)

    note : it's possible to display a m2m using : {% displaym2m object.m2m_relation [with "path/to/template"]%}
        default template :
            app/model/m2m.html if existe
            else use {% display object %} (see jute befor) for display each object in the list


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



Bugs:
====

    If you have som bugs with the menu, reboot the server (to destroy the cache). generaly bugs are fixed with this.


Resum:
======


To display:
-----------

    {% load Kraggne_tags %}

    init(add page var to context far other tags) : {% getmenu %}

    breadcrumb: {% breadcrumb ["slug"] [include_self=True] %}
    {% breadcrumb ["slug"] into "slug_object" [include_self=True] %}
    {% breadcrumb ["slug"] with "templatename.html" [include_self=True] %}
    {% breadcrumb ["slug"] with "templatename.html" as "variable" [include_self=True] %}

    Menu: {% menu ["slug"] [include_self=True level_min=0 level_nb=0] %}
    {% menu ["slug"] into "slug_object" [include_self=True level_min=0 level_nb=0] %}
    {% menu ["slug"] with "templatename.html" [include_self=True level_min=0 level_nb=0] %}
    {% menu ["slug"] with "templatename.html" as "variable" [include_self=True level_min=0 level_nb=0] %}

    Submenu : {% sousmenu ["slug"] [include_self=False level_min=0 level_nb=1] %}
    {% sousmenu ["slug"] into "slug_object" [include_self=False level_min=0 level_nb=1] %}
    {% sousmenu ["slug"] with "templatename.html" [include_self=False level_min=0 level_nb=1] %}
    {% sousmenu ["slug"] with "templatename.html" as "variable" [include_self=False level_min=0 level_nb=1] %}

    in a forloop
    {% last == obj2 var %}
    {% last != obj2 var %}
    {% last <= obj2 var %}
    {% last < obj2 var %}
    {% last >= obj2 var %}
    {% last > obj2 var %}

    Model: {% try_display obj [with template_path ] %} => prefer use {% display my_model_instance %}
    Form : {% displayform form_instance %}

    Pagination :{% pagination %}


    {% load flatblocks %}
    create a instance of model in template: (use {% display object %} with default template
    {% gblock "slug" for "appname.modelname" %}
    {% gblock "slug" for "appname.modelname" into "slug_object" %}
    {% gblock "slug" for "appname.modelname" with "templatename.html" %}
    {% gblock "slug" for "appname.modelname" with "templatename.html" as "variable" %}

    get a list of a specifique model: (internaly use {% display object %} on each object with default template
    {% glist "slug" for "appname.modelname" %}
    {% glist "slug" for "appname.modelname" into "slug_object" %}
    {% glist "slug" for "appname.modelname" with "templatename.html" %}
    {% glist "slug" for "appname.modelname" with "templatename.html" as "variable" %}


    Model : {% display my_model_instance %}
    ManyToMany : {% displaym2m object.m2m %}


    {% load contentblocks %}
    create or get a containeur and display  it (use {% display object %} on each)

    {% containeur "slug" [css_class=None] [page=None] %}
    {% containeur "slug" into "slug_name" [css_class=None] [page=None] %}
    {% containeur "slug" with "template_path" [css_class=None] [page=None] %}
    {% containeur "slug" with "template_path" as "variable_name" [css_class=None] [page=None] %}

    default use: {% containeur page.slug %}


    {% load gblocks %}
    {{filename|get_file_extension}}
    {{filename|get_file_name}}



To custom the display:
----------------------

[app],[model] and [classname] are always in lower case

    Model : 
        overwrite [app]/[model]/object.html => use with {% display object %}
        the self.display() methode          => use with {% display object %} if existe
        flatblocks/unknow_object.html       => default (display all the field of the object)

    ManyToMany :
        overwrite [app]/[model]/m2m.html   => use with {% displaym2m object.m2m %}
        flatblocks/m2m.html                => default that use internaly {% display object %} for each in the query

    List(glist):
        overwrite [app]/[model]/object_list.html => all object in same template
        overwrite [app]/[model]/object.html      => for each object
        Kraggne/flatblocks/object_list.html      => default (all)

    Form:
        [app]/forms/[classname].html        => use with {% displayform form %}
        Kraggne/form.html                  => default

    ListView: extends base.html and put code in {% block page.body %}
        [app]/[model]/list.html            => use with Generic[Form]ListView (internaly use {% display object %} on each object in the list )
        Kraggne/generic[Form]ListPage.html => default
        Use pagination too (see after)
    
    DetailView: extends base.html and put code in {% block page.body %}
        [app]/[model]/detail.html         => use with Generic[Form]DetailView
        Kraggne/generic[Form]DetailPage.html => default

    FormView: extends base.html and put code in {% block page.body %}
        see Form
        Kraggne/genericForm[Detail/List]Page.html => default

    Pagination:
        Kraggne/pagination.inc.html

    Breadcrumb:
        Kraggne/breadcrumb.html

    Menu (nav):
        Kraggne/menu.html



Views:
------
    If you want to create your own view, just herit of one of this:

    GenericViewContextMixin:
        slug = "your slug here"

    class GenericView(GenericViewContextMixin,TemplateView):
        template_name = "Kraggne/genericPage.html"
        slug = "your slug here"

    class GenericDetailView(GenericView):
        template_name = "Kraggne/genericDetailPage.html"
        slug = "your slug here"
        model = "yourmodel"
        #url need (?P<pk>[*0-9]+) or <slug> (exepte if your model have a self.get_object_from_url(**kwargs) methode)
    
    class GenericFormView(GenericViewContextMixin,FormView):
        template_name = "Kraggne/genericFormPage.html"
        slug = "your slug here"
        form_class = "your form class"
        #form.save(commit=True,request=self.request) or form.save(commit=True) for modelForm only

    class GenericListView(GenericViewContextMixin,ListView):
        template_name = "Kraggne/genericListPage.html"
        slug = "your slug here"
        model = "yourmodel"
        paginate_by = 10 #default is model.paginate_by if existe

    class GenericListFormView(GenericListView,FormMixin,ProcessFormView):
        template_name = "Kraggne/genericListFormPage.html"
        slug = "your slug here"
        model = "yourmodel"
        paginate_by = 10 #default is model.paginate_by if existe
        form_class = "your form class"
        #form.save(commit=True,request=self.request) or form.save(commit=True) for modelForm only
    
    
    class GenericDetailFormView(GenericDetailView,FormMixin,ProcessFormView):
        template_name = "Kraggne/genericDetailFormPage.html"
        slug = "your slug here"
        model = "yourmodel"
        form_class = "your form class"
        #url need (?P<pk>[*0-9]+) or <slug> (exepte if your model have a self.get_object_from_url(**kwargs) methode)
        #form.save(commit=True,request=self.request) or form.save(commit=True) for modelForm only


    
    Don't forget to add the correct slug="kraggne-[db-slug-view]" on your view and {% getmenu %} on your base.html (for menu,sousmenu,breadcrumb,containeur tags)





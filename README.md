Kraggne
=======

Un projet de cms django


Instalation:
-----------
     
    in your INSTALLED_APPS add :
        'mptt'
        'Kraggne'

        optional:
        'Kraggne.contrib.django_generic_flatblocks'
        'Kraggne.contrib.gblocks'

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


Breadcrumb:
----------

    {% load Kraggne_tags %}

    {% breadcrumb ["slug"] [include_self=True] %}
    {% breadcrumb ["slug"] into "slug_object" [include_self=True] %}
    {% breadcrumb ["slug"] with "templatename.html" [include_self=True] %}
    {% breadcrumb ["slug"] with "templatename.html" as "variable" [include_self=True] %}


Generic Block (need django_generic_flatblocks): 
-------------

    {% load  generic_flatblocks %}

    {% gblock "test-block" for "gblocks.Text"  %}
    {% gblock "test-block" for "gblocks.Text" into object  %}
    {% gblock "test-block" for "gblocks.Text" with tempate_path %}
    {% gblock "test-block" for "gblocks.Text" with template_path as varable_name %}

    you can also display a block using:
    {% display generic_object %}


Generic List (need django_generic_flatblocks):
----------------------------------------------

    {% load  generic_flatblocks %}

    {% glist "test-list" for "gblocks.Text"  %}
    {% glist "test-list" for "gblocks.Text" into object  %}
    {% glist "test-list" for "gblocks.Text" with tempate_path %}
    {% glist "test-list" for "gblocks.Text" with template_path as varable_name %}

    you can also display a list using:
    {% display generic_object_list %}


Exemple:
-------


    {% load Kraggne_tags %}

    {% block page.title %}{% endblock %}
    <hr/>
    {% breadcrumb %}
    <hr/>
    {% menu level_min=-1 level_nb=3 include_self=False %}

CMS:
===
     
     You will have to add to you INSTALL_APPS:
     
        'Kraggne.contrib.django_generic_flatblocks'
        'Kraggne.contrib.gblocks'

    in your urls.py add :
        (r'',            include('Kraggne.urls')),

     Using the admin, you can creat your menu, and chose CMS option. This option will auto creat the nex url,
     and use a specifique view.
     By default, the "Kraggne/genericPage.html" is use to diplay the page.
     If you want a other, you just have to associate a template to the itemPage you want (using admin).
     You can also add a form (one form for one page). The default template use for this view is "Kraggne/genericFormPage.html"
     You can use a other. the for is contain in the "form" context var.
     
     If you need mor vars, you can add them using the PageVars model.
     It auto add (name) and (name)_list to the context where name is the name of the nex var created.
     You can also add filter kwargs using the query_args field.
     
     the same way is use with gblock an glist, but not store by the same way, and they could be use out of the cms pages.
     



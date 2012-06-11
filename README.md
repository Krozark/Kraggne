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


Menu Gestion:
------------
    {% load Kraggne_tags %}

    {% menu ["slug"] [include_self=True level_min=0 level_nb=0] %}
    {% menu ["slug"] into "slug_object" [include_self=True level_min=0 level_nb=0] %}
    {% menu ["slug"] with "templatename.html" [include_self=True level_min=0 level_nb=0] %}
    {% menu ["slug"] with "templatename.html" as "variable" [include_self=True level_min=0 level_nb=0] %}


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

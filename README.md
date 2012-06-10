Kraggne
=======

Un projet de cms django


Menu Gestion:
------------

    {% menu ["slug"] [include_self=True level_min=0 level_nb=0] %}
    {% menu ["slug"] into "slug_object" [include_self=True level_min=0 level_nb=0] %}
    {% menu ["slug"] with "templatename.html" [include_self=True level_min=0 level_nb=0] %}
    {% menu ["slug"] with "templatename.html" as "variable" [include_self=True level_min=0 level_nb=0] %}


Breadcrumb:
----------

    {% breadcrumb ["slug"] [include_self=True] %}
    {% breadcrumb ["slug"] into "slug_object" [include_self=True] %}
    {% breadcrumb ["slug"] with "templatename.html" [include_self=True] %}
    {% breadcrumb ["slug"] with "templatename.html" as "variable" [include_self=True] %}



Exemple:
-------

    {% load Kraggne_tags %}

    {% block page.title %}{% endblock %}
    <hr/>
    {% breadcrumb %}
    <hr/>
    {% menu level_min=-1 level_nb=3 include_self=False %}

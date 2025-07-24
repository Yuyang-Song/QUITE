# related_query_name&#39;s default / fallback behaviour has changed in Django 1.10
[Link to question](https://stackoverflow.com/questions/47524839/related-query-names-default-fallback-behaviour-has-changed-in-django-1-10)
**Creation Date:** 1511848527
**Score:** 1
**Tags:** python, django
## Question Body
<p>I am updating a project from Django 1.8 to Django 1.11. It's a somewhat mature / complex project with a lot of models and queries.</p>

<p>It seems that a backwards incompatible change was made in Django 1.10, namely the default behaviour of <code>ForeignKey.related_query_name</code>. In Django 1.10, <code>related_query_name</code> falls back to the model's <code>default_related_name</code> - in Django 1.8 this was not the case. This change is apparent in the docs:</p>

<p>Django 1.9: <a href="https://docs.djangoproject.com/en/1.9/ref/models/fields/#django.db.models.ForeignKey.related_query_name" rel="nofollow noreferrer">https://docs.djangoproject.com/en/1.9/ref/models/fields/#django.db.models.ForeignKey.related_query_name</a></p>

<p>Django 1.10: <a href="https://docs.djangoproject.com/en/1.10/ref/models/fields/#django.db.models.ForeignKey.related_query_name" rel="nofollow noreferrer">https://docs.djangoproject.com/en/1.10/ref/models/fields/#django.db.models.ForeignKey.related_query_name</a></p>

<p>Almost all of my models have <code>default_related_name</code> defined, yet no <code>ForeignKey</code>s have <code>related_query_name</code> set. This means that essentially all of my database queries that traverse relationships are invalid!</p>

<p>Am I doomed to rewrite all my queries, or add <code>related_query_name</code> to everything? Or is there some way to retain the old functionality?</p>


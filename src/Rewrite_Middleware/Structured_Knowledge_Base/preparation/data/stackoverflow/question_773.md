# How do you override Django&#39;s admin app_index?
[Link to question](https://stackoverflow.com/questions/41770603/how-do-you-override-djangos-admin-app-index)
**Creation Date:** 1484938714
**Score:** 2
**Tags:** django, django-admin
## Question Body
<p>I'm very familiar with how to override Django's admin <em>templates</em>, but I haven't been able to find any instructions on how to properly override the context available to said templates.  For example this page:</p>

<pre><code>/admin/users/
</code></pre>

<p>The style for this page can be overridden by creating a file at:</p>

<pre><code>root/users/templates/admin/users/app_index.html
</code></pre>

<p>But what if I want to do some more Python-level stuff <em>before</em> the template is loaded?  Specifically in my case I want to generate a sort of dashboard for <code>/admin/users/</code> and for that I'll need to run a rather elaborate query.</p>

<p>Now I know I could hack this by creating a template tag that does the query for me, but frankly that's pretty dirty as you're hitting the database from a template, so I'd like to do this <em>better</em> if such a way exists.</p>

<p>If however you can state with confidence (and convincingly) that this simply can't be done without rewriting <code>django.contrib.admin.sites.AdminSite.app_index</code>, then I'll flag your answer as correct and go with my ugly hack.</p>

## Answers
### Answer ID: 76520132
<p>An Alternative might be to override the app_index.html template and use an inclusion tag or any other custom templatetag to incorporate your custom view.</p>

### Answer ID: 41771029
<p>It can be done, and without rewriting <code>app_index</code>. Since <code>AdminSite</code> is intended to be customized through subclassing.</p>

<p>Looking at the <code>AdminSite</code> implementation, you can see <code>app_index</code> has a keyword argument <code>extra_context</code>. You can utilize this for your purposes to avoid rewriting as follows</p>

<pre><code>from django.contrib.admin import AdminSite

class MyAdmin(AdminSite):
    def app_index(self, request, app_label, extra_context=None):
        if not extra_context:
            extra_context = {}
        extra_context['my_new_key'] = 'val'

        super().app_index(request, app_label, extra_context=extra_context)
</code></pre>

<p>The problem then arises that you would need to instantiate your custom site and use it to set your urls and register model admins. If this is inconvenient as suggested by Alasdair, you might consider <a href="https://stackoverflow.com/a/30056258">this</a>.</p>

<p>All that being said, you will still hit the database on the request anyway, similar to your concern with the tag. Only caching would solve that.</p>


# Create custom template tag in Django?
[Link to question](https://stackoverflow.com/questions/48146580/create-custom-template-tag-in-django)
**Creation Date:** 1515400178
**Score:** 0
**Tags:** python, django, python-2.7, django-1.10
## Question Body
<p>I have next models in my Django project.</p>

<p><strong>models.py:</strong></p>

<pre><code>class Document(models.Model):
    name = models.TextField(blank=True, null=True)

    def get_children(self):
        return [dc.child for dc in DocumentClosure.objects.filter(parent=self)]

class DocumentClosure(models.Model):
    parent = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="closures_as_parent",
        db_column='parent_id',
        blank=True,
        null=True
    )

    child = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="closures_as_child",
        db_column='child_id',
        blank=True,
        null=True
    )

    level = models.IntegerField(
        default=0,
        blank=True,
        null=True
    )
</code></pre>

<p>Next models create 2 table in database with <code>"Closure Table"</code> architecture. 
<em>DocumentClosure</em> store information about <em>ancestors</em> and <em>descendants</em>. I want to show tree in template as it make <code>django-mptt</code> application.</p>

<p>I started with next code. Now I need to rewrite <code>get_children()</code> method based on my current models. Can someone help me with this method?!</p>

<p><strong>template:</strong></p>

<pre><code>&lt;ul&gt;
    {% recursetree documents %}
        &lt;li&gt;
            {{ node.name }}
            &lt;ul class="children"&gt;
                {{ children }}
            &lt;/ul&gt;
        &lt;/li&gt;
    {% endrecursetree %}
&lt;/ul&gt;
</code></pre>

<p><strong>custom_tag.py:</strong></p>

<pre><code>from django import template

register = template.Library()

@register.tag
def recursetree(parser, token):
    bits = token.contents.split()
    if len(bits) != 2:
        raise template.TemplateSyntaxError(_('%s tag requires a queryset') % bits[0])
    queryset_var = template.Variable(bits[1])
    template_nodes = parser.parse(('endrecursetree',))
    parser.delete_first_token()
    return RecurseTreeNode(template_nodes, queryset_var)


class RecurseTreeNode(template.Node):
    def __init__(self, template_nodes, queryset_var):
        self.template_nodes = template_nodes
        self.queryset_var = queryset_var

    def _render_node(self, context, node):
        bits = []
        context.push()
        for child in node.get_children():  # get_children() initialized in models.py file | rewrite this method
            bits.append(self._render_node(context, child))
        context['node'] = node
        context['children'] = mark_safe(''.join(bits))
        rendered = self.template_nodes.render(context)
        context.pop()
        return rendered

    def render(self, context):
        queryset = self.queryset_var.resolve(context)
        roots = queryset
        bits = [self._render_node(context, node) for node in roots]
        return ''.join(bits)
</code></pre>

<p><strong>EDIT:</strong>
After <code>python manage.py runserver</code> command in console I see the endless repetitive queries to the database. But after some time it raise error:</p>

<pre><code>Traceback (most recent call last):
File "/Users/nurzhan_nogerbek/Virtualenvs/py2714/lib/python2.7/site-packages/django/core/handlers/exception.py", line 41, in inner
    response = get_response(request)
  File "/Users/nurzhan_nogerbek/Virtualenvs/py2714/lib/python2.7/site-packages/django/core/handlers/base.py", line 217, in _get_response
    response = self.process_exception_by_middleware(e, request)
  File "/Users/nurzhan_nogerbek/Virtualenvs/py2714/lib/python2.7/site-packages/django/core/handlers/base.py", line 215, in _get_response
    response = response.render()
  File "/Users/nurzhan_nogerbek/Virtualenvs/py2714/lib/python2.7/site-packages/django/template/response.py", line 107, in render
    self.content = self.rendered_content
  File "/Users/nurzhan_nogerbek/Virtualenvs/py2714/lib/python2.7/site-packages/django/template/response.py", line 84, in rendered_content
    content = template.render(context, self._request)
  File "/Users/nurzhan_nogerbek/Virtualenvs/py2714/lib/python2.7/site-packages/django/template/backends/django.py", line 66, in render
    return self.template.render(context)
  File "/Users/nurzhan_nogerbek/Virtualenvs/py2714/lib/python2.7/site-packages/django/template/base.py", line 207, in render
    return self._render(context)
  File "/Users/nurzhan_nogerbek/Virtualenvs/py2714/lib/python2.7/site-packages/django/template/base.py", line 199, in _render
    return self.nodelist.render(context)
  File "/Users/nurzhan_nogerbek/Virtualenvs/py2714/lib/python2.7/site-packages/django/template/base.py", line 990, in render
    bit = node.render_annotated(context)
  File "/Users/nurzhan_nogerbek/Virtualenvs/py2714/lib/python2.7/site-packages/django/template/base.py", line 957, in render_annotated
    return self.render(context)
  File "/Users/nurzhan_nogerbek/Virtualenvs/py2714/lib/python2.7/site-packages/django/template/loader_tags.py", line 177, in render
    return compiled_parent._render(context)
  File "/Users/nurzhan_nogerbek/Virtualenvs/py2714/lib/python2.7/site-packages/django/template/base.py", line 199, in _render
    return self.nodelist.render(context)
  File "/Users/nurzhan_nogerbek/Virtualenvs/py2714/lib/python2.7/site-packages/django/template/base.py", line 990, in render
    bit = node.render_annotated(context)
  File "/Users/nurzhan_nogerbek/Virtualenvs/py2714/lib/python2.7/site-packages/django/template/base.py", line 957, in render_annotated
    return self.render(context)
  File "/Users/nurzhan_nogerbek/Virtualenvs/py2714/lib/python2.7/site-packages/django/template/loader_tags.py", line 177, in render
    return compiled_parent._render(context)
  File "/Users/nurzhan_nogerbek/Virtualenvs/py2714/lib/python2.7/site-packages/django/template/base.py", line 199, in _render
    return self.nodelist.render(context)
  File "/Users/nurzhan_nogerbek/Virtualenvs/py2714/lib/python2.7/site-packages/django/template/base.py", line 990, in render
    bit = node.render_annotated(context)
  File "/Users/nurzhan_nogerbek/Virtualenvs/py2714/lib/python2.7/site-packages/django/template/base.py", line 957, in render_annotated
    return self.render(context)
  File "/Users/nurzhan_nogerbek/Virtualenvs/py2714/lib/python2.7/site-packages/django/template/loader_tags.py", line 72, in render
    result = block.nodelist.render(context)
  File "/Users/nurzhan_nogerbek/Virtualenvs/py2714/lib/python2.7/site-packages/django/template/base.py", line 990, in render
    bit = node.render_annotated(context)
  File "/Users/nurzhan_nogerbek/Virtualenvs/py2714/lib/python2.7/site-packages/django/template/base.py", line 957, in render_annotated
    return self.render(context)
  File "/Users/nurzhan_nogerbek/Virtualenvs/py2714/lib/python2.7/site-packages/django/template/loader_tags.py", line 72, in render
    result = block.nodelist.render(context)
  File "/Users/nurzhan_nogerbek/Virtualenvs/py2714/lib/python2.7/site-packages/django/template/base.py", line 990, in render
    bit = node.render_annotated(context)
  File "/Users/nurzhan_nogerbek/Virtualenvs/py2714/lib/python2.7/site-packages/django/template/base.py", line 957, in render_annotated
    return self.render(context)
  File "/Users/nurzhan_nogerbek/Virtualenvs/py2714/lib/python2.7/site-packages/django/template/loader_tags.py", line 216, in render
    return template.render(context)
  File "/Users/nurzhan_nogerbek/Virtualenvs/py2714/lib/python2.7/site-packages/django/template/base.py", line 209, in render
    return self._render(context)
  File "/Users/nurzhan_nogerbek/Virtualenvs/py2714/lib/python2.7/site-packages/django/template/base.py", line 199, in _render
    return self.nodelist.render(context)
  File "/Users/nurzhan_nogerbek/Virtualenvs/py2714/lib/python2.7/site-packages/django/template/base.py", line 990, in render
    bit = node.render_annotated(context)
  File "/Users/nurzhan_nogerbek/Virtualenvs/py2714/lib/python2.7/site-packages/django/template/base.py", line 957, in render_annotated
    return self.render(context)
  File "/Applications/Projects/web/project/documents/templatetags/documents_tags.py", line 41, in render
    bits = [self._render_node(context, node) for node in roots]
  File "/Applications/Projects/web/project/documents/templatetags/documents_tags.py", line 31, in _render_node
    bits.append(self._render_node(context, child))
File "/Applications/Projects/web/project/documents/models.py", line 117, in get_children
    return [dc.child for dc in DocumentClosure.objects.filter(parent=self)]
  File "/Users/nurzhan_nogerbek/Virtualenvs/py2714/lib/python2.7/site-packages/django/db/models/query.py", line 250, in __iter__
    self._fetch_all()
  File "/Users/nurzhan_nogerbek/Virtualenvs/py2714/lib/python2.7/site-packages/django/db/models/query.py", line 1118, in _fetch_all
    self._result_cache = list(self._iterable_class(self))
  File "/Users/nurzhan_nogerbek/Virtualenvs/py2714/lib/python2.7/site-packages/django/db/models/query.py", line 53, in __iter__
    results = compiler.execute_sql(chunked_fetch=self.chunked_fetch)
  File "/Users/nurzhan_nogerbek/Virtualenvs/py2714/lib/python2.7/site-packages/django/db/models/sql/compiler.py", line 871, in execute_sql
    sql, params = self.as_sql()
  File "/Users/nurzhan_nogerbek/Virtualenvs/py2714/lib/python2.7/site-packages/django/db/backends/oracle/compiler.py", line 21, in as_sql
    with_col_aliases=with_col_aliases,
  File "/Users/nurzhan_nogerbek/Virtualenvs/py2714/lib/python2.7/site-packages/django/db/models/sql/compiler.py", line 436, in as_sql
    where, w_params = self.compile(self.where) if self.where is not None else ("", [])
  File "/Users/nurzhan_nogerbek/Virtualenvs/py2714/lib/python2.7/site-packages/django/db/models/sql/compiler.py", line 373, in compile
    sql, params = node.as_sql(self, self.connection)
  File "/Users/nurzhan_nogerbek/Virtualenvs/py2714/lib/python2.7/site-packages/django/db/models/sql/where.py", line 79, in as_sql
    sql, params = compiler.compile(child)
  File "/Users/nurzhan_nogerbek/Virtualenvs/py2714/lib/python2.7/site-packages/django/db/models/sql/compiler.py", line 373, in compile
    sql, params = node.as_sql(self, self.connection)
  File "/Users/nurzhan_nogerbek/Virtualenvs/py2714/lib/python2.7/site-packages/django/db/models/fields/related_lookups.py", line 127, in as_sql
    return super(RelatedLookupMixin, self).as_sql(compiler, connection)
  File "/Users/nurzhan_nogerbek/Virtualenvs/py2714/lib/python2.7/site-packages/django/db/models/lookups.py", line 169, in as_sql
    lhs_sql, params = self.process_lhs(compiler, connection)
  File "/Users/nurzhan_nogerbek/Virtualenvs/py2714/lib/python2.7/site-packages/django/db/models/lookups.py", line 162, in process_lhs
    db_type = self.lhs.output_field.db_type(connection=connection)
  File "/Users/nurzhan_nogerbek/Virtualenvs/py2714/lib/python2.7/site-packages/django/db/models/fields/related.py", line 991, in db_type
    return self.target_field.rel_db_type(connection=connection)
  File "/Users/nurzhan_nogerbek/Virtualenvs/py2714/lib/python2.7/site-packages/django/db/models/fields/__init__.py", line 951, in rel_db_type
    return IntegerField().db_type(connection=connection)
  File "/Users/nurzhan_nogerbek/Virtualenvs/py2714/lib/python2.7/site-packages/django/db/models/fields/__init__.py", line 166, in __init__
    if isinstance(choices, collections.Iterator):
  File "/Users/nurzhan_nogerbek/Virtualenvs/py2714/bin/../lib/python2.7/abc.py", line 141, in __instancecheck__
    subtype in cls._abc_negative_cache):
  File "/Users/nurzhan_nogerbek/Virtualenvs/py2714/bin/../lib/python2.7/_weakrefset.py", line 75, in __contains__
    return wr in self.data
RuntimeError: maximum recursion depth exceeded in cmp
</code></pre>

<p>Lets say I have such tree. <strong>Example</strong>:</p>

<pre><code>A
|
 - B
   |
    - C
</code></pre>

<p><strong>document</strong> table:</p>

<pre><code>id | parent_id | name
1  |           | A
2  | 1         | B
3  | 2         | C
</code></pre>

<p>Finally <strong>document_closure</strong> table:</p>

<pre><code>id | parent_id | child_id | level
1  | 1         | 1        | 0
2  | 2         | 2        | 0
3  | 3         | 3        | 0
4  | 1         | 2        | 1
5  | 2         | 3        | 1
6  | 1         | 3        | 2
</code></pre>

## Answers
### Answer ID: 48151379
<p>Select all <code>DocumentClosure</code> objects that have your <code>Document</code> as <code>parent</code> and return their children.</p>

<p>Return a list with their linked child <code>Document</code> like this:</p>

<pre><code>class Document(models.Model):
    name = models.TextField(blank=True, null=True)

    def get_children(self):
        return [dc.child for dc in DocumentClosure.objects.filter(parent=self)]
</code></pre>

<p>You should consider renaming the <code>related_name</code> of both <code>ForeignKey</code> relations on <code>DocumentClosure</code> - they create properties with confusing names. <code>Document.parents</code> returns a <code>Queryset</code> of <code>DocumentClosure</code> objects where the given <code>Document</code> is the parent. One would expect it to include the parents of the current document. Maybe something like <code>closures_as_parent</code> and <code>closures_as_child</code> fits better.</p>


# How to avoid import-time database access in Django?
[Link to question](https://stackoverflow.com/questions/43326132/how-to-avoid-import-time-database-access-in-django)
**Creation Date:** 1491835193
**Score:** 4
**Tags:** python, django, database
## Question Body
<p>My Django app has a number of categories for things which I store in a <code>Category</code> model. I reference these frequently in code, and so I've found it useful to have a module with references ("constants") to these categories and groups of them, so typos will fail fast. This also provides the benefit of caching. And finally, it's the actual model so it has all the related functionality. It looks something like this:</p>

<pre><code>def load_category(name):
  return Category.objects.get(name=name)

DOGS = load_category("dogs")
CATS = load_category("cats")
</code></pre>

<p>However, this results in import-time database access and causes various issues. After adding a new category with a reference like this, I must run a data migration before <code>./manage.py</code> will function. I just hit a new problem while switching to using Django's test framework, which is that these load from the default (e.g., dev or prod) database rather than the test one as explicitly mentioned in <a href="https://docs.djangoproject.com/en/1.10/topics/testing/overview/#the-test-database" rel="nofollow noreferrer">this warning</a>.</p>

<blockquote>
  <p>If your code attempts to access the database when its modules are
  compiled, this will occur before the test database is set up, with
  potentially unexpected results. For example, if you have a database
  query in module-level code and a real database exists, production data
  could pollute your tests. It is a bad idea to have such import-time
  database queries in your code anyway - rewrite your code so that it
  doesn’t do this.</p>
</blockquote>

<p><strong>What's the best pattern for obtaining the benefits of these references while avoiding the import-time database access?</strong></p>

<p>One possible solution is a proxy pattern which returns a pseudo-Category which forwards all the model's functionality but does not access the database until it's necessary. I'd like to see how others have solved this problem with this approach or another solution.</p>

<p>(Related but different question: <a href="https://stackoverflow.com/questions/19714521/django-test-finding-data-from-your-production-database-when-running-tests">Django test. Finding data from your production database when running tests?</a>)</p>

<p><strong>Final Approach</strong></p>

<p>The approach by @kevin-christopher-henry's worked well for me. However, in addition to fixing these declared references, I also had to delay access to the references from other code. Here I found two approaches helpful. </p>

<p>First, I discovered <a href="https://docs.djangoproject.com/en/1.10/topics/testing/overview/#the-test-database" rel="nofollow noreferrer">Python Lazy Object Proxy</a>. This simple object takes a factory function as input, which is lazily executed to produce the wrapped object.</p>

<pre><code>MAP_OF_THINGS = Proxy(lambda: {
        DOG: ...
        CAT: ...
})
</code></pre>

<p>A similar way of accomplishing the same thing was pushing code into factory functions decorated with <a href="https://stackoverflow.com/a/815160/317110">memoize</a> so they'd only be executed once.</p>

<p>NOTE: I initially tried to use the Proxy object above as a direct solution to my problem of lazy access to model objects. However, despite being <em>very</em> good imitations, when querying and filtering on these objects I got: </p>

<pre><code>TypeError: 'Category' object is not callable
</code></pre>

<p>Sure enough, <code>Proxy</code> returns <code>True</code> for <code>callable</code> (even though docs say this doesn't guarantee it's callable). It seems that Django queries are just too smart and bound to find something incompatible with a phoney model.  </p>

<p>For your application, <code>Proxy</code> might be good enough.</p>

## Answers
### Answer ID: 56752309
<p>I've used lazy_object_proxy (wich works with passed function but without passed arguments) in companion with functools.partial like below:</p>

<pre><code>import lazy_object_proxy
from functools import partial

def load_category(name):
  # prepare an argument-less runnable function
  loader = partial(Category.objects.get, name)

  # pass the function to the proxy
  return lazy_object_proxy.Proxy(loader)

DOGS = load_category("dogs")
CATS = load_category("cats")
</code></pre>

### Answer ID: 43334810
<p>I've run into the same issue myself, and agree that it would be great to have some best practices here.</p>

<p>I ended up with an approach based on the <a href="https://docs.python.org/3/howto/descriptor.html" rel="nofollow noreferrer">descriptor protocol</a>:</p>

<pre><code>class LazyInstance:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.instance = None

    def __get__(self, obj, cls):
        if self.instance is None:
            self.instance, _ = cls.objects.get_or_create(*self.args, **self.kwargs)

        return self.instance
</code></pre>

<p>Then in my model classes I have some special objects:</p>

<pre><code>class Category(models.Model):
    name = models.CharField()

    DOGS = LazyInstance(name="dogs")
    CATS = LazyInstance(name="cats")
</code></pre>

<p>So nothing happens at import time. The first time the special object is accessed, the relevant instance is looked up (and created, if necessary) and cached.</p>

### Answer ID: 43327239
<p>There's not much you can do with module-level variables, since you cannot override their access functions. However you can do that for class and instance variables via <a href="https://docs.python.org/2/reference/datamodel.html#object.__getattribute__" rel="nofollow noreferrer"><code>__getattribute__</code></a>. You can use that to load your categories lazily:</p>

<pre><code>class Categories(object):
    _categories = {'DOGS': 'dogs', 'CATS': 'cats'}
    def __getattribute__(self, key):
        try:
            return super(Categories, self).__getattribute__(key)
        except AttributeError:
            pass
        try:
            value = load_category(self._categories[key])
        except KeyError:
            raise AttributeError(key)
        setattr(self, key, value)
        return value

Categories = Categories()  # Shadow class with singleton instance
</code></pre>

<p>Instead of <code>module.DOGS</code> you would then use <code>module.Categories.DOGS</code>. Upon the first access the category is loaded and stored for future lookups.</p>


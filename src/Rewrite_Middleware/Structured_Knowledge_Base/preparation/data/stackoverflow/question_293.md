# Django test. Finding data from your production database when running tests?
[Link to question](https://stackoverflow.com/questions/19714521/django-test-finding-data-from-your-production-database-when-running-tests)
**Creation Date:** 1383245766
**Score:** 2
**Tags:** django, testing, document
## Question Body
<p>Django 1.5 document about testing said:</p>

<p>Finding data from your production database when running tests?</p>

<p>If your code attempts to access the database <strong>when its modules are compiled</strong>, this will occur before the test database is set up, with potentially unexpected results. For example, if you have a database query <strong>in module-level code</strong> and a real database exists, production data could pollute your tests. It is a bad idea to have such <strong>import-time database queries</strong> in your code anyway - rewrite your code so that it doesn’t do this.</p>

<p>Can someone explain bold text which i can't understand. Thank you. </p>

## Answers
### Answer ID: 19739308
<p>You are reading this: <a href="http://djbook.ru/rel1.5/topics/testing/overview.html" rel="nofollow">http://djbook.ru/rel1.5/topics/testing/overview.html</a></p>

<p>That looks like one of those collaborative online books that might contain awkward passages.</p>

<p>Firstly, your settings file sets up a database:</p>

<pre><code>DATABASES = {
'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME':    'myDB' ...
</code></pre>

<p>When you run tests, the test runner reads that NAME, prepends "test_" to get "test_myDB", and creates a blank database for tests to play with.</p>

<p>But the test runner does this only after the module is loaded (NOT "compiled"). So...</p>

<pre><code>from django.test import TestCase

# Don't use the database here; it's still myDB

class SimpleTest(TestCase):

    def setUp(self):
           # We are all about the test_myDB database, here
        self.user = User.objects.create_user(
            username='zaphod',
            email='zaphod@...',
            password='beeblebrox',
        )
</code></pre>

<p>Another detail: Unless you are insane, and are deving and testing directly on your production server, myDB is NOT the "production database." A better name would be the "development database."</p>


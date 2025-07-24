# Unit testing with Symfony 2 and database
[Link to question](https://stackoverflow.com/questions/21581096/unit-testing-with-symfony-2-and-database)
**Creation Date:** 1391613403
**Score:** 0
**Tags:** php, sql, unit-testing, symfony
## Question Body
<p>I'm trying to understand the unit tests when a database is involved. My classes heavily depends on a database to do their work. I already had a look at many many answers here on stackoverflow and on the internet in general, but I'm not really happy with what I found.</p>

<p>One of the common problems that I see when a database is involved (MySQL in my case) is that the tests are really really long to execute and one possible solution is to use SQLite.</p>

<p>I can't use it everywhere in the tests because some classes uses RAW queries instead of the Doctrine querybuilder to bypass the limitation of unknown datetime functions. SQLite has a different set of functions for date values and this means that to use it in the tests I should rewrite my queries twice, one for MySQL and one for SQLite.</p>

<p>I decided then to stick with MySQL, but creating and dropping the schema every time a test runs takes so much time. I know that the SchemaTool class can handle the creation of a subset of the schema: would be a good solution to create only the tables I really need in the test suite or should I always use the full schema?</p>

<p><strong>Example of the part of code (pseudo-code) I'm trying to test</strong></p>

<pre><code>NotificationManagerClass
    constructor(EntityManager)
    loadNotifications()
    deleteNotification()
    updateNotification()
</code></pre>

<p>as you can see, I inject the entity manager in the constructor of the class. The class is a service registered in the Symfony container. In the controller I then get this service and use its methods. Inside the methods I use the querybuilder because I must have access to some other services and a repository isn't container-aware. How can I decouple more than this my class? I can't think a way to do it</p>

## Answers
### Answer ID: 21581746
<p>You mix a lot of words together, which don't all have the meaning you gave them. A quick summary of the words:</p>

<ul>
<li><strong>Unit tests</strong> - Tests only <em>one</em> class. It doesn't test nor instantiate any other classes (it uses mocks or stubs for them). It shouldn't be using a database, it should mock doctrine instead.</li>
<li><strong>Web tests</strong> - These tests test how multiple classes work together using database. These are often quite slow, so you don't want to have very many very specific tests here.</li>
<li><strong>MySQL</strong> and <strong>SQLite</strong> are both just database driver. SQLite is as slow as MySQL and it really doesn't matter which one you use (well, it does matter, you have to use the same driver as you use in production)</li>
</ul>

<p>You can't mock everything, because you decided to use raw mysql functions (bad choice)... Always avoid to use mysql queries inside classes. Use either Doctrine (there are a lot of simple ways to bypass the unknown datetime functions) or put the raw queries in the Repository and mock the repository.</p>

<p>In short:</p>

<ul>
<li>Don't use anything other than the tested object in unit tests (mock/stub everything else)</li>
<li>Web Tests should be using production tools</li>
<li>Don't use mysql directly in a class</li>
</ul>

### Answer ID: 21581836
<p>Test involving a database is not a unit test. Your repositories should be tested with integration or functional tests (or acceptance if you write such).</p>

<p>If you have many tests involving database, that probably means you took a wrong turn somewhere, either with:</p>

<ul>
<li>code design - your classes are coupled to the database</li>
<li>deciding how to test - writing too many integration tests instead of unit tests</li>
</ul>

<p>Might be worth looking into the test pyramid: <a href="http://martinfowler.com/bliki/TestPyramid.html" rel="nofollow">http://martinfowler.com/bliki/TestPyramid.html</a> </p>

<p>By looking into how to speed up your tests you'll only continue walking the wrong path. The solution is to write more unit tests and less integration tests. Unit tests are fast, independent and isolated, therefore harder to break. Integration tests are more fragile and slow. Look into <a href="http://pragprog.com/magazines/2012-01/unit-tests-are-first" rel="nofollow">FIRST properties of unit tests</a>.</p>

<p>Btw: SQLite is a dead end. It doesn't behave like mysql as it doesn't support constraints.</p>

<p>Your example class could be modelled as:</p>

<pre class="lang-php prettyprint-override"><code>class NotificationManager
{
    public function __construct(MyNotificationRepository $repository, MyFabulousService $service)
    {}

    // ... other methods
}
</code></pre>

<p>This way you can inject fakes of both repository and your service and test the NotificationManager in isolation.</p>

<p>There's no much value in unit testing query builders as you'd be testing doctrine instead of your code. It is also hard, since the query class is declared final. You can test if queries return correct results functionally. There's gonna be lot less functional tests needed if you unit test your classes properly. </p>

<p>If you made the MyNotificationRepository an interface, you could even decouple from doctrine. </p>


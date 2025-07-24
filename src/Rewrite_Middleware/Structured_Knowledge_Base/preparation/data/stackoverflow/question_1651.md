# How do I write object classes effectively when dealing with table joins?
[Link to question](https://stackoverflow.com/questions/2741041/how-do-i-write-object-classes-effectively-when-dealing-with-table-joins)
**Creation Date:** 1272578024
**Score:** 3
**Tags:** php, oop, class
## Question Body
<p>I should start by saying I'm not now, nor do I have any delusions I'll ever be a professional programmer so most of my skills have been learned from experience very much as a hobby. </p>

<p>I learned PHP as it seemed a good simple introduction in certain areas and it allowed me to design simple web applications. </p>

<p>When I learned about objects, classes etc the tutor's basic examnples covered the idea that as a rule of thumb each database table should have its own class. While that worked well for the photo gallery project we wrote, as it had very simple mysql queries, it's not working so well now my projects are getting more complex. If I require data from two separate tables which require a table join I've instead been ignoring the class altogether and handling it on a case by case basis, OR, even worse been combining some of the data into the class and the rest as a separate entity and doing two queries, which to me seems inefficient. </p>

<p>As an example, when viewing content on a forum I wrote, if you view a thread, I retrieve data from the threads table, the posts table and the user table. The queries from the user and posts table are retrieved via a join and not instantiated as an object, whereas the thread data is called using my Threads class.</p>

<p>So how do I get from my current state of affairs to something a little less 'stupid', for want of a better word. Right now I have a DB class that deals with connection and escaping values etc, a parent db query class that deals with the common queries and methods, and all of the other classes (Thread, Upload, Session, Photo and ones thats aren't used Post, User etc ) are children of that. </p>

<p>Do I make a big posts class that has the relevant extra attributes that I retrieve from the users (and potentially threads) table?<br>
Do I have separate classes that populate each of their relevant attributes with a single query? If so how do I do that?<br>
Because of the way my classes are written, based on what I was taught,  my db update row method, or insert method both just take the attributes as an array and update all of that, if I have extra attributes from other db tables in each class then how do I rewrite those methods as obbiously updating automatically like that would result in errors?  </p>

<p>In short I think my understanding is limited right now and I'd like some pointers when it comes to the fundamentals of how to write more complex classes.</p>

<p>Edit:  </p>

<p>Thanks for the answers so far they've given me lots of pointers and thoughts and a lot of reading material. What I would like though is maybe an idea of how different people have decided to handle a simple table join with any amount of classes? Did you add attributes to the classes? Query from outside the class then pass the results into each class? Something else? </p>

## Answers
### Answer ID: 2741209
<p>Entire books have been written about how to design a set of classes to fit a database schema.</p>

<p>Long story short: there is no one-size-fits-all way to do it, you have to make a lot of design decisions about the trade offs you want to make on an application-by-application basis.</p>

<p>You can find a library or framework to help, keywords: ActiveRecord, ORM (Object Relational Mapper)</p>

<p>P.S. You have no idea the potential for soul-killing analysis paralysis and over designing you can get into. Do the simplest thing that can possibly work for your app.</p>

<p>Code sample for my (below) comment:</p>

<pre><code>$post = new PublishedPost($data);
$edit = $post-&gt;setTitle($newTitle);
$edit-&gt;save();
</code></pre>

### Answer ID: 2741161
<p>This is too broad to be answered without going into epic length. </p>

<p>Basically, there is four prominent Data Source Architectural Patterns from <a href="http://martinfowler.com/eaaCatalog/index.html" rel="nofollow noreferrer">Patterns of Enterprise Architecture</a>: <a href="http://martinfowler.com/eaaCatalog/tableDataGateway.html" rel="nofollow noreferrer">Table Data Gateway</a>, <a href="http://martinfowler.com/eaaCatalog/rowDataGateway.html" rel="nofollow noreferrer">Row Data Gateway</a>, <a href="http://martinfowler.com/eaaCatalog/activeRecord.html" rel="nofollow noreferrer">Active Record</a> and <a href="http://martinfowler.com/eaaCatalog/dataMapper.html" rel="nofollow noreferrer">Data Mapper</a>. These can be found implemented in the common <a href="http://www.php-frameworks.net/" rel="nofollow noreferrer">php frameworks</a> in some variation. These are easy to grasp and implement.</p>

<p>Where it gets difficult is when you start to tackle the <a href="http://en.wikipedia.org/wiki/Object-relational_impedance_mismatch" rel="nofollow noreferrer">impedance mismatch</a> between the database and the business objects in your application. To do so, there are a number of Object-Relational Behavioral, Structural and Metadata Mapping Patterns, like Identity Maps, Lazy Loading, Query Objects, Repositories, etc. Explaining these is beyond scope. They cover almost 200 pages in PoEAA.</p>

<p>What you can look at is <a href="http://www.doctrine-project.org/" rel="nofollow noreferrer">Doctrine</a> or <a href="http://www.propelorm.org/" rel="nofollow noreferrer">Propel</a> - the two most well known <a href="http://en.wikipedia.org/wiki/Object-relational_mapping" rel="nofollow noreferrer">PHP ORM</a> - that implement most of these patterns and which you could use in your application to replace your current database access handling.</p>

### Answer ID: 2741073
<p>Many of your worries can be answered by inspecting the existing solutions found in well-tested frameworks such as <a href="http://cakephp.org/" rel="nofollow noreferrer">CakePHP</a>, <a href="http://www.symfony-project.org/" rel="nofollow noreferrer">symfony</a> and <a href="http://framework.zend.com/" rel="nofollow noreferrer">Zend Framework</a>. Examining their approaches and peeking under the hood should shed light on your questions. Who knows? You may even decide to write future projects using them!</p>

<p>They've spent years putting their heads together to tackle these problems. Take advantage!</p>

### Answer ID: 2741102
<p>Checkout <a href="http://www.doctrine-project.org/" rel="nofollow noreferrer">Doctrine:</a></p>

<p>Here is an example of a forum application using Doctrine.</p>

<p><a href="http://www.doctrine-project.org/documentation/manual/1_2/en/real-world-examples#forum-application" rel="nofollow noreferrer">http://www.doctrine-project.org/documentation/manual/1_2/en/real-world-examples#forum-application</a></p>


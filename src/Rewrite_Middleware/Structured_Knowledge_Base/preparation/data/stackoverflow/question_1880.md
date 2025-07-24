# Is an ORM overkill for our needs? If not, which one?
[Link to question](https://stackoverflow.com/questions/10826535/is-an-orm-overkill-for-our-needs-if-not-which-one)
**Creation Date:** 1338429531
**Score:** 1
**Tags:** php, orm, doctrine, propel
## Question Body
<p>I work for a website with a large legacy codebase that has hundreds of custom mysql queries, using the original PHP MySQL API.  For security reasons, we'd like to rewrite our models to remove the directly written queries.</p>

<p>Our original plan was to simply rewrite our queries to use the PDO PHP extension for accessing our database. However, we then started looking into ORMs like Propel and Doctrine, had actually made the decision to try using Propel.</p>

<p>However, I'm starting to wonder whether this is overkill for us--rewriting our models is in itself a massive job. To make this work, we are going to try to duplicate the existing function of our models--this means returning all of our data in associative arrays. But, if we do that, are we basically losing most of the benefit of going to an ORM system?</p>

<p>Another wrinkle is that our system depends heavily on caching the results of queries, and invalidating the results with a system of namespaces. We thought at first that it might not be too hard to extend Propel to handle results caching, but an internet search suggest that that is not something people are normally doing with Propel; moreover, Doctrine appears to have results caching built in.</p>

<p>If we are returning results our of queries as associative arrays, and not taking full advantage of the data objects, are there other benefits we might get from using Doctrine or Propel that make it worth the overhead of working with an ORM? The best argument I can think of is that, after we've finished overhauling our model, we could at least start trying to take full advantage of the ORM in new systems, and could perhaps in the future start overhauling older systems to also take advantage of it.</p>

<p>So the question is: Are we best off using PDO directly if we aren't going to return objects with the ORM? Or, if there are other advantages to using the ORM, is the built-in caching on Doctrine a killer feature (if we need caching), or is this something that could be added to Propel?</p>

## Answers
### Answer ID: 12051992
<blockquote>
  <p>Are we best off using PDO directly if we aren't going to return objects with the ORM?</p>
</blockquote>

<p>At some point, everyone drops the ORM and relies on PDO only. That's because hydration is expensive.</p>

<blockquote>
  <p>Or, if there are other advantages to using the ORM, is the built-in caching on Doctrine a killer feature (if we need caching), or is this something that could be added to Propel?</p>
</blockquote>

<p>You can use either Propel or Doctrine and decide to return objects, not arrays. You can also use a caching layer on top of one of these ORMs. Doctrine provides a caching layer in their "commons" package (I'm talking about Doctrine2, Doctrine 1 is no more supported anyway). Propel doesn't provide a caching layer because there are a lot of existing libraries for that.</p>

<p>Using a caching layer with Propel is doable, just pick a caching lib and you'll be ready. Btw, Propel provides a <a href="http://www.propelorm.org/behaviors/query-cache.html" rel="nofollow">query cache behavior</a> if you want to cache generated SQL queries.</p>

<p>To sum up, using a caching layer is not tied to an ORM but to your application.</p>


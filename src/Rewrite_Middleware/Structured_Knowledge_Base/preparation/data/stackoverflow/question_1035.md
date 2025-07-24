# Why should MVC for websites require a single point of entry?
[Link to question](https://stackoverflow.com/questions/5596520/why-should-mvc-for-websites-require-a-single-point-of-entry)
**Creation Date:** 1302272634
**Score:** 4
**Tags:** php, model-view-controller
## Question Body
<p>I see many MVC implementations for websites have a single-entry point such as an index.php file and then parses the URL to determine which controller to run. This seems rather odd to me because it involves having to rewrite the URL using Apache rewrites and with enough pages that single file will become bloated.</p>

<p>Why not instead just to have the individual pages be the controllers? What I mean is if you have a page on your site that lists all the registered members then the <code>members.php</code> page users navigate to will be the controller for the members. This php file will query the members model for the list of members from the database and pass it in to the members view.</p>

<p>I might be missing something because I have only recently discovered MVC but this one issue has been bugging me. Wouldn't this kind of design be preferable because instead of having one bloated entry-file that all pages unintuitively call the models and views for a specific page are contained, encapsulated, and called from its respective page?</p>

## Answers
### Answer ID: 65980775
<p><strong>Software engineers are influencing the single point of entry paradigm. &quot;Why not instead just to have the individual pages be the controllers?&quot;</strong></p>
<p>Individual pages are already <code>Controllers</code>, in a sense.</p>
<ol>
<li>In PHP, there is going to be some boilerplate code that loads for every HTTP request: autoloader require statement (PSR-4), error handler code, sessions, and if you are wise, wrapping the core of your code in a try/catch with <code>Throwable</code> as the top exception to catch. By centralizing code, you only need to make changes in one place!</li>
</ol>
<p>True, the centralized PHP will use at least one require statement (to load the autoloader code), but even if you have many require statements they will all be in one file, the index.php (not spread out over a galaxy of files on under the document root).</p>
<ol start="2">
<li>If you are writing code with security in mind, again, you may have certain encoding checks/sanitizing/validating that happens with every request. Using values in <code>$_SERVER</code> or <code>filter_input_array()</code>? Then you might as well centralize that.</li>
</ol>
<p>The bottom line is this. The more you do on every page, the more you have a good reason to centralize that code.</p>
<p>Note, that this way of thinking leads one down the path of looking at your website as a web application. From the web application perspective, a single point of entry is justifiable because a problem solved once should only need to be modified in one place.</p>

### Answer ID: 6271267
<p>A single entry point certainly has its advantages, but you can get pretty much the same benefit from a central required file at the top of every single page that handles database connections, sessions, etc. It's not bloated, it conforms to DRY principles (except for that one require line), it seperates logic and presentation and if you change file locations, a simple search and replace will fix it.</p>

<p>I've used both and I can't say one is drastically better or worse for my purposes.</p>

### Answer ID: 5596857
<p>When deeplinking directly into the controllers when using an MVC framework it eliminates the possibility of implementing controller plugins or filters, depending on the framework you are using. Having a single point of entry standardizes the bootstrapping of the application and modules and executing previously mentioned plugins before a controller is accessed.</p>

<p>Also Zend Framework uses its own URL rewriting in the form of Routing. In the applications that use Zend Framework I work on have an .htaccess file of maybe 6 lines of rewriterules and conditions.</p>

### Answer ID: 5596774
<p>From my experience, having a single-entry point has a couple of notorious advantages:</p>

<p>It eases centralized tasks such as resource loading (connecting to the db or to a memcache server, logging execution times, session handling, etc). If you want to add or remove a centralized task, you just have to change a singe file, which is the index.php.</p>

<p>Parsing the URL in PHP makes the "virtual URL" decoupled from the physical file layout on your webserver. That means that you can easily change your URL system (for example, for SEO purposes, or for site internationalization) without having to actually change the location of your scripts in the server.</p>

<p>However, sometimes having a singe-entry point can be a waste of server resouces. That applies obviously to static content, but also when you have a set of requests that have a very specific purpose and just need a very little set of your resorces (maybe they don't need DB access for instance). Then you should consider having more than one entry point. I have done that for the site I am working on. It has an entry point for all the "standard" dynamic contents and another one for the calls to the public API, which need much less resources and have a completely different URL system.</p>

<p>And a final note: if the site is well-implemented, your index.php doesn't have to become necessarily bloated :)</p>

### Answer ID: 5596716
<p>it is all about being DRY, if you have many php files handling requests you will have duplicated code. That just makes for a maintenance nightmare.</p>

<p>Have a look at the 'main' index page for CakePHP, <a href="https://github.com/cakephp/cakephp/blob/master/app/webroot/index.php" rel="nofollow">https://github.com/cakephp/cakephp/blob/master/app/webroot/index.php</a></p>

<p>no matter how big the app gets, i have never needed to modify that. so how can it get bloated?</p>


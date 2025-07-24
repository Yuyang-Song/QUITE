# Symfony: Issuing request to another bundle in same app to get data
[Link to question](https://stackoverflow.com/questions/28955215/symfony-issuing-request-to-another-bundle-in-same-app-to-get-data)
**Creation Date:** 1425954905
**Score:** 1
**Tags:** php, symfony, architecture, soa
## Question Body
<p>I have a bit of a dilema, I have a Symfony2 app and in it I've built a bundle which is just a REST Api layer to my database.</p>

<p>The thing is that I have another bundle, and I want it to perform some updates in the database. I don´t want to rewrite code to perform the same tasks in this new bundle. </p>

<p>Is it feasible for me to issue requests to my api from another bundle within the same app? Would it take longer than making the queries from this new bundle? I'm concerned about performance and scalability.</p>

<p>To exemplify I'll write an example:</p>

<p>Bundle A contains a REST api, one of the resources that it exposes is "Person" which allows GET, POST, PUT, DELETE. This resource maps to a database table.</p>

<p>In the other hand, there is Bundle B, which has to run some tasks and finally update some users in my database. I don't want to copy my Person Entity from the api bundle to this bundle to perform the update.</p>

<p>What would you do in this situation?</p>

## Answers
### Answer ID: 28957913
<p>I think You should communicate between bundles using services (Dependency Injection). <br> </p>

<blockquote>
  <p><a href="http://symfony.com/doc/current/book/service_container.html" rel="nofollow">Symfony2 Service Container Docs</a><br></p>
</blockquote>

<p>If you register service in one bundle, and you named it "myDataLayerService", you can inject it into services of another bundle(Like any other services - request service, entity manager, router, etc.) or, you can get it in controller very easilly: <br> 
<code>$myDBLayer = $this-&gt;get("myDataLayerService");</code><br>
And then you call any public function created in your service. </p>

<pre><code>$myDBLayer-&gt;persistObjectToDatabase($veryNiceObject);
</code></pre>

<p>TL;DR: Registered Symfony services in one bundle, are available in any other bundle.</p>


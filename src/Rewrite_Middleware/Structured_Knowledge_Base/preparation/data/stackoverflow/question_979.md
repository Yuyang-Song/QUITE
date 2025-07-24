# Extending existing RESTful API using Node.js
[Link to question](https://stackoverflow.com/questions/52899302/extending-existing-restful-api-using-node-js)
**Creation Date:** 1539979954
**Score:** 2
**Tags:** node.js, rest, http, express, tomcat
## Question Body
<p>I am currently running a web service on an Apache Tomcat servlet container. The web service has a base URL and exposes my applications data using the following structure:</p>

<p><a href="http://[hostname]:[port]/path/to/root/[db_table_name]/[primary_key]?fields=name" rel="nofollow noreferrer">http://[hostname]:[port]/path/to/root/[db_table_name]/[primary_key]?fields=name</a>,...</p>

<p>An HTTP GET call to a URL like the one above would return a JSON formatted string.</p>

<p>Though the documentation for my application describes this as a RESTful API, I am confused because I was under the impression that true RESTful APIs do not use query strings. Rather, as I understand it, a true restful API provides a uniform structure, in the form of resource endpoints. </p>

<p>My questions relate to how I can create a custom API to leverage the existing API using Node.js. I do not want to rewrite the application logic or database calls; I just need to know how I can create the API calls using Node.js (possibly using Express or some other framework) and let the existing API handle the request. </p>

<p>For example, I could write Node.js code using the Express module that has several routes, these routes would handle client requests that in turn would call the existing API (i.e. /path/to/root/[table_name]/[pk]... and return the response. </p>

<ol>
<li>If my Apache Tomcat server is listening on port 8080, how would I deploy my Node.js server to listen on another port and then redirect requests to the existing WS URL on port 8080.</li>
<li>Does the Express framework support explicitly specifying a root path (such as <a href="http://localhost:3000/path/to/root/[table_name]/[pk]" rel="nofollow noreferrer">http://localhost:3000/path/to/root/[table_name]/[pk]</a>) as the default root path?</li>
<li>Finally, I know REST APIs support CRUD operations. In the case of a POST method, does Express (or Node.js) have built-in logic to handle duplicate POST requests so that duplicate records don't get created in the database.</li>
</ol>

<p>I'm reading through different article and tutorials on REST but I think I'm missing something. Any information or advice that can take me in the right direction would be much appreciated.</p>

## Answers
### Answer ID: 52905778
<p>there's a lot to cover here but I'll try to cover your three questions. Since you have mentioned using Express I will answer assuming that Express is the framework you are using.</p>

<ol>
<li><p>If you are using Express, you can choose which port to listen to when you start the server, so you can choose any port that you like at that point (see <a href="https://expressjs.com/en/api.html#app.listen" rel="nofollow noreferrer">here</a>).
If you need to redirect a request you can do so easily with <code>res.redirect()</code> (see <a href="https://expressjs.com/en/api.html#app.listen" rel="nofollow noreferrer">here</a>). However, you could also call the other web service directly, retrieve the data and return it to the client instead of redirecting them if you prefer. That would require some more code to make the http requests in node.js though.</p></li>
<li><p>I am not 100% sure if this is the answer to your question, but there are ways to add a "base path" or namespace to all of your routes. I found <a href="http://bulkan-evcimen.com/using_express_router_instead_of_express_namespace.html" rel="nofollow noreferrer">this example</a> where various namespaces are used but in your case you only need one which applies to all routes.</p></li>
<li><p>I don't think there is a built-in way to do this. The best I can think of is potentially creating some kind of ID for the request so that if it is sent twice you could use this to check but it's far from ideal.</p></li>
</ol>

<p>I would like to add that I'm not sure where the idea that query parameters not being RESTful comes from? I think query parameters are fine because that is how you query! Otherwise you couldn't ask for the right data from your RESTful API. Let's say you have a /posts endpoint and you want to get the posts of a particular user (user ID = 1). The RESTful way to do this would be to issue a GET request to /posts?user=1.</p>

<p>Hope this helps!</p>


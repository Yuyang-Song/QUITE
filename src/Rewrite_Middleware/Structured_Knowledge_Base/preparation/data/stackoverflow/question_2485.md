# URL rewriting Node js - dynamic URLs
[Link to question](https://stackoverflow.com/questions/36678623/url-rewriting-node-js-dynamic-urls)
**Creation Date:** 1460907773
**Score:** -3
**Tags:** javascript, node.js, dynamic-url
## Question Body
<p>This seems to be a Noob question, but still i dont know how to go about with this. 
Im using node js for my server side development and recently came across SEO friendly URLs. 
How do i rewrite the URLS which are something like www.abc.com/meet_team.html to 
www.abc.com/meet-the-team/ </p>

<p>One answer would be to use controllers and to route to html pages. This works fine for static web pages.</p>

<p>My problem is with dynamic data. To quote an example, Lets say, yts.ag page has movies stored in the db and it gets retrieved and the url changes dynamically.</p>

<p>For example : www.yts.ag/movies/the-revenant - > This would pick up details about the movie revenant. If the change it to movies/the-dark-knight, it would do so accordingly. Here movies would be the controller, In my Node code, i would handle it something like this.</p>

<pre><code>app.get('/:controller/:movieName', func(req, res){
      // get controller and movie name from req object and query from DB and respond back.
}) 
</code></pre>

<p>Now the problem is, i would have stored the name of movie as "The Revenant" in the DB. I would be getting the movie name from the GET request as "the-revenant". How do i query this from the database? </p>

<p>Should i parse the param first? strip the hyphen and then pass it to the DB or any other solution? </p>

<p>Please help me on this. I dont know whether this is the right approach.
Thanks in advance.</p>

## Answers
### Answer ID: 36678732
<p>It is as you describe. Now you have to retrieve the movie from the slug reference.</p>

<p>Look for mongo or mysql</p>


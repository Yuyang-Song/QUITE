# ASP.NET 4.0 URL Rewriting: How to deal with the IDs
[Link to question](https://stackoverflow.com/questions/5060534/asp-net-4-0-url-rewriting-how-to-deal-with-the-ids)
**Creation Date:** 1298241004
**Score:** 3
**Tags:** asp.net, .net-4.0, url-rewriting
## Question Body
<p>I have just started adding the new .NET 4.0 URL Rewriting into my project. I have a question.</p>

<p>Let's say I have a Article.aspx that displays, well, articles. I made a route for it in the Global.asax:</p>

<pre><code>routes.MapPageRoute("article-browse", "article/{id}", "~/Article.aspx");
</code></pre>

<p>So the link consists of the article's id which is, obviously, not a very nice, nor SEO friendly link. I would like to display the Article's title in the link, instead of the ID.</p>

<p>Do I have to pass the whole title in the parameter (instead of the id) and then make a SQL query that searches for a database record with the matching title? That sounds scary. Maybe there is some way to do something similar to the Eval() methods, that would change the title into an ID?</p>

<p>Thank you very much!</p>

## Answers
### Answer ID: 5060569
<p>There is nothing to prevent you from including both the ID (for quick SQL retrieval) and the article's title in the link (for SEO purposes). This is exactelly how stackoverflow is handling the routing (check the address for this question).</p>

<pre><code>routes.MapPageRoute("article-browse", "article/{id}/{title}", "~/Article.aspx");
</code></pre>

<p>Obviously, the title after the ID is not necessary to display the page (you only use the ID to fetch the article), but everytime you generate the link in your site, generate it with the title, and the bots will use that when indexing your pages.</p>

<p>Oh, and you might also want to create a method that translates your title into a URL-friendly string.Like making all lowercase, converting spaces and other characters to '-',etc.</p>


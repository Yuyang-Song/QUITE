# ViewState, QueryStrings and their effect on SEO
[Link to question](https://stackoverflow.com/questions/3884520/viewstate-querystrings-and-their-effect-on-seo)
**Creation Date:** 1286474889
**Score:** 0
**Tags:** asp.net, seo, query-string, viewstate
## Question Body
<p>Well, to start with, I'm a novice ASP.Net/C# programmer, and had an experience only of a couple of projects during college and a couple of freelancing projects when I was recruited by a startup company to build their ASP.Net based website. I've just abut completed the website, and now since the company is not able to find a worthy enough SEO, I'm expected to do our site's SEO as well(which is a totally new experience for me). Did I mention that I'm the only Web Developer here?</p>

<p>So, now as you'd expect a novice programmer having no concern for future SEO needs, I built up the site without giving due consideration to any of the SEO enhancement techniques.</p>

<p>The Problems:</p>

<ul>
<li><p>ViewState - When is it required? Is it really required if I'm not creating any controls on the fly? I'm using DataControls though. And the website(the pages visible to the user not the CMS), is purely information based. Also, if I disable a control(ex: DataList)'s viewstate, will the viewstate of controls inside it also get disabled?(which is what I'd like actually)</p></li>
<li><p>QueryStrings - Now comes the toughest part, I've used Query Strings to the extent that you can say that the website is QueryString driven, which unfortunately enough is not a good thing for SEO. To make matters worse, the QueryStrings for some pages are not uniform. For ex- In some cases the querystring may have variables A, B, and C, while in other cases it can have variables M, B, C and probably not all the three variables in some cases. Now, I know that I'd have to do url rewriting but these query strings have dynamic data fetched from the database tables of size more than 10,000 rows. So would I have to create functions for url rewriting and use regex to separate wheat from whaff?</p></li>
</ul>

<p>All help is deeply Appreciated.</p>

<p>Regards
Anchit</p>

## Answers
### Answer ID: 3884902
<p>The classic issue is not being able to get to all the pages through simple links/GET.</p>

<p>The issue with the above is any postback, as those happen through a post (which in some cases is started through javascript).</p>

<p>I haven't had issues people mention about the Query String and SEO. But maybe its just that I tend to have fewer uniform query string parameters.</p>


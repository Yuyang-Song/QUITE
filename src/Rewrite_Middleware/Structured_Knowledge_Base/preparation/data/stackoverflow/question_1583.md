# Rebinding functions on dynamic content using jQuery and AJAX
[Link to question](https://stackoverflow.com/questions/506764/rebinding-functions-on-dynamic-content-using-jquery-and-ajax)
**Creation Date:** 1233660593
**Score:** 0
**Tags:** ajax, asynchronous, jquery
## Question Body
<p>I'm in the process of building a back-end admin panel for a site and I'm having an issue with the jQuery and AJAX code is use to build the page.</p>

<p>On load, I bind actions to certain table fields allowing users to add or delete a colour or size. When they submit the form, I empty the table and use AJAX to generate a new one, then put the new table into the form. </p>

<p>Unfortunately, the new form isn't (as I expected) affected by the $(document).ready function. I am wondering if there's a way of either re-calling the document.ready function to bind the actions to the new elements in the page or alternatively to call a jQuery function without going through the document.ready function.</p>

<p>I could rewrite the jQuery function in vanilla javascript and call it that way but I far prefer to reuse the jQuery code if at all possible.</p>

<p>I've found some stuff about how to do it using ASP.NET and UpdatePanels but this site is in PHP and it uses a basic AJAX query to insert into the database, refetch the results then build up the table of results.</p>

<p>Any ideas?</p>

## Answers
### Answer ID: 506800
<p>Have you tried using <a href="http://docs.jquery.com/Events/live" rel="nofollow noreferrer">live events</a>? This is for 1.3 only.</p>

<p>For previous versions you can use the <a href="http://plugins.jquery.com/project/livequery" rel="nofollow noreferrer">live query</a> plugin. With this you can run match and unmatch listeners (run code when a match occurs). You can also force the evaluation of bindings using the livequery.run method.</p>

<p>Update:</p>

<p>For anyone that finds this now, the live method has been deprecated as of 1.7.  Live had some major nagging issues and so was replaced with a more powerful function: <a href="http://api.jquery.com/on/" rel="nofollow noreferrer">on</a>.  Even if you aren't on 1.7 yet you should highly consider at least using <a href="http://api.jquery.com/delegate/" rel="nofollow noreferrer">delegate</a> (jquery 1.4.2) as live has some harsh limits</p>

### Answer ID: 506945
<p>live events seem the best answer; but if not, you should simplify the <code>$(document).ready()</code> function to make it call an initialization function.  later on, after loading your AJAX content, you just call it again.</p>


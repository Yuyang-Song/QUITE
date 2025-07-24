# Ideal way of showing context sensitive help on partial view load in MVC
[Link to question](https://stackoverflow.com/questions/35607561/ideal-way-of-showing-context-sensitive-help-on-partial-view-load-in-mvc)
**Creation Date:** 1456331149
**Score:** 0
**Tags:** jquery, ajax, asp.net-mvc, partial-views, asp.net-mvc-partialview
## Question Body
<p>I have an application with several partial views, some are loaded via ajax, some are not. </p>

<p>There are some context sensitive notes for each of these partial views stored in the database.</p>

<p>When each of these partial views load, I want to load their help text inside a div and show it on a side bar.</p>

<p>I want to do this with minimal rewrite of existing partial views.</p>

<p>Some of the approaches I have considered</p>

<p>1) Add a layout to all partial views. Add a data-helpText attribute to all divs encapsulating a partial view. In the layout page, on document.ready, I will read the data-helpText attribute and fire off an ajax query to load the help text from the database.</p>

<p>2) Add a helptext attribute to the viewbag of each partial view. Read this attribute and fire off an ajax query to read help text. Problem with this approach is the next partial view will overwrite the attribute. Is there any way I could create a collection in viewbag and dynamically append to this from each partial view ?</p>

<p>Neither of the above approaches seem all that great to me. Has anyone else done something like this or has an idea on what approach I should take ?</p>

<p>Thanks in advance...</p>


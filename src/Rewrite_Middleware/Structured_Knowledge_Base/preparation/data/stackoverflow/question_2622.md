# OOP PHP architecture
[Link to question](https://stackoverflow.com/questions/43139734/oop-php-architecture)
**Creation Date:** 1490960236
**Score:** 0
**Tags:** php, oop, architecture
## Question Body
<p>Sorry if my question is wishy-washy.</p>

<p>I'm new to OOP. What I'm wondering is how "object orientated" should I go with my new project. Although I'm not up on all the tech lingo I think I have a reasonable understanding of classes/objects as data types. What is preventing me from launching right into it is the uncertainty about the "right" architecture.</p>

<p>For example, right now I have a standard class that can be instantiated as an object holding the database handle and has methods for getRow, getRows, insertRow, updateRow to which queries and parameters are sent and that all works.</p>

<p>It just doesn't seem correct that I'm just creating the $db object in the top of a page and then handing that to every object that needs it.</p>

<p>The system I'm building has distinct page types, e.g blog pages, product pages, checkout, etc. I'm using apache rewrites to send all requests to a single page on which I will switch out the code that is executed.</p>

<p>Would it seem correct to instantiate an object for each type.</p>

<pre><code>if($pageType = "blog-post"){
  $page = new BlogPost($db);
}
else if($pageType = "product-listings"){
  $page = new ProductListing($db);
}

$page-&gt;SendToView();
</code></pre>

<p>If I ensure that the $page object always has a SendToView method that worries about how the page is displayed.</p>

<p>Are there more than one implementations of the MVC pattern? I assumed MVC is what I need but when I looked for tutorials they seem completely different but all refer to themselves as MVC.</p>


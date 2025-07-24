# displaying AJAX based Please Wait on multiple pages
[Link to question](https://stackoverflow.com/questions/1078149/displaying-ajax-based-please-wait-on-multiple-pages)
**Creation Date:** 1246605522
**Score:** 0
**Tags:** php, mysql, ajax, page-loading-message
## Question Body
<p>I am making a data entry form in php/mysql. There i have added many dropdowns and auto complete textboxes, which query the database asynchronously and fetch the data. I wanted to inform the user that some kind of interaction between client and server is been taking palce, so i placed an element in hidden form</p>

<pre><code> &lt;div id="wait" style="background-color:white;position:absolute;top:240px;left:360px;width:70px;height:50px;visibility:hidden;border: 1px solid black;padding:20px;"&gt;
 &lt;img src="images/wait.gif" style="position:relative;top:0px;left:25px"&gt;&lt;br /&gt;&lt;br /&gt;Please wait...
 &lt;/div&gt;
</code></pre>

<p>and in the method handleHttpResponse for the ajax component i did the following</p>

<pre><code>if (http.readyState == 4) {
  document.getElementById('wait').style.visibility = "hidden";
  alert('The server script has now completed');
} else {
  document.getElementById('wait').style.visibility = "visible";
}
</code></pre>

<p>The function above is in the script file ajax.js which is included in the current page, and everypage where ever ajax is required.</p>

<p>Now this worked fine for me for the single document, but i had the following queries</p>

<ul>
<li><p>If i wish to have similar operation that whenever on ANY PAGE an AJAX request is performed, the user must be shown with the message "PLEASE WAIT along with playing the animation". How must i rewrite my modules so that i don't have to place the DIV on each and everypage. How can i go about it?</p>

<ul>
<li><p>I wish to add a similar feature but it must happen before the page loads, and it should show the Progress Bar as well, how can i go about it</p></li>
<li><p>Say my current page makes use of this feature at 3 places, simultaneously, will it show 3 Please Wait Messages or not?</p></li>
</ul></li>
</ul>

<p>Hope my question is clear enough.
Thanks</p>

## Answers
### Answer ID: 1775733
<p>There's a way to achieve what you are trying to do. For example, if you are using PHP, you can place your HTML in a .inc or .php file and include that wherever you want, even in multiple pages. </p>

<ol>
<li><p>So, if using PHP, try something like this:</p>

<pre><code>&lt;?php //inc_loader.php ?&gt;&lt;div id="wait" style="background-color:white;position:absolute;top:240px;left:360px;width:70px;height:50px;visibility:hidden;border: 1px solid black;padding:20px;"&gt;
 &lt;img src="images/wait.gif" style="position:relative;top:0px;left:25px"&gt;&lt;br /&gt;&lt;br /&gt;Please wait...
 &lt;/div&gt;
</code></pre></li>
</ol>

<p>Now simply include the above file wherever you want to, like:</p>

<pre><code>&lt;?php include("inc_loader.php"); ?&gt;
</code></pre>

<p>The code to include can vary depending upon the Server side language you are using. </p>

<p>2.Also it's not recommended to use the same code in multiple places within the same document as you are using id="wait". An id should be unique within a document, so using it at multiple places does not hold it's meaning. If you want to avoid duplication, then you may try using class i.e. class="wait" if that's something that could help you. </p>

<p>Let us know if that helped you.</p>


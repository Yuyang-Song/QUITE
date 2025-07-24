# submit a form when hitting the browser back button
[Link to question](https://stackoverflow.com/questions/13471461/submit-a-form-when-hitting-the-browser-back-button)
**Creation Date:** 1353408061
**Score:** 1
**Tags:** php, javascript
## Question Body
<p>I have a page for asking queries to an SQL database. Its only purpose is to allow students to exercise. Depending on the students activity the page rewrites itself with new content so that the student may enter a query, have the resulting table shown or get an error message.</p>

<p>All is working through forms that post data to the same page.</p>

<p>However, if a student uses the back button or the forward button (after hitting the back button) data gets lost as I cleanse the $_POST variable content to get ready for new action.</p>

<p>There is, however, a "go back" button that assembles data to restore the previous page by POSTing the required data. Is it possible to use some kind of technique, javascript, html5, PHP or whatever to actually submit the form that posts the assembled data when hitting the browser back button?</p>

<p>I am using HTML 5, PHP 5 and some JavaScript (not JQuery but if it gives me an option ...)</p>

## Answers
### Answer ID: 13471553
<p>As suggested in the comments you could store the post data in the session, for example every time a new query is posted you could add it:</p>

<pre><code>$_SESSION['queries'][] = $_POST;
</code></pre>

<p>Then you could allow the users to go back / forward through this with some form of loop:</p>

<pre><code>&lt;ul&gt;
&lt;?php foreach($_SESSION['queries'] as $k =&gt; $v) : ?&gt;
    &lt;li&gt;Some link structure&lt;/li&gt;
&lt;?php endforeach; ?&gt;
&lt;/ul&gt;
</code></pre>

### Answer ID: 13471529
<p>you can use the html5 storage since if user not fill the full form or close the browser the data will lost on close browser and not submit it form not fill </p>

<p>to check html5 storage </p>

<pre><code> function supports_html5_storage() {
          try {
            return 'localStorage' in window &amp;&amp; window['localStorage'] !== null;
          } catch (e) {
            return false;
          }
        }
</code></pre>

<p>use onkeyup to store  like</p>

<pre><code>  $("#title").keyup(function(){

            var articel_title =  $("#title").val();
            localStorage.setItem("articel_title",articel_title);
             localStorage.getItem("articel_title");
        });
</code></pre>

<p>and next time when user open the form just show the content stored</p>

<p>to clear use</p>

<pre><code>localStorage.removeItem("articel_title");
</code></pre>


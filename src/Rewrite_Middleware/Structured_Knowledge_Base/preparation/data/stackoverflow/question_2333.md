# Classic ASP and MySQL database - I want to add an age restriction on a form with if then and else statement. Is this possible?
[Link to question](https://stackoverflow.com/questions/29836394/classic-asp-and-mysql-database-i-want-to-add-an-age-restriction-on-a-form-with)
**Creation Date:** 1429833294
**Score:** 1
**Tags:** mysql, asp-classic, datediff
## Question Body
<p>So I am working in a classic ASP environment with a MySQL database. I want to add in a query to a form so that it adds an age restriction of being at least 13 years old. Here's what I was attempting to throw into the code:</p>

<pre><code>If DATEDIFF("yyyy",now(), Person_DateOfBirth) &gt; 12 Then
    Response.write "You are over 12"
Else
    Response.write "You are under 12"
End if
</code></pre>

<p>I am attempting to use the Datediff attribute to limit the age result. The now() variable is set as the current date, the <code>Person_DateOfBirth</code> variable is the selection that they choose on the form. Then im attempting to write a response on the screen depending on the value from the diffdate. </p>

<p>When this code is inserted into the query, there is no response at all. </p>

<p>I need help rewriting this code so it functions correctly, or if someone has another resolution in Classic ASP, that would be great. </p>

<p>Thanks! </p>

## Answers
### Answer ID: 29838054
<p>The code requires the <a href="http://www.w3schools.com/asp/coll_form.asp" rel="nofollow">ASP Form Collection</a> to access the "Person_DateOfBirth" variable submitted through the form.  </p>

<p><strong>Example Code</strong></p>

<p><em>default.asp</em></p>

<pre><code>&lt;html&gt;
    &lt;body&gt;
        &lt;form action="submit.asp" method="post"&gt;
        My age is &lt;input type="text" name="Person_DateOfBirth"&gt;
        &lt;input type="submit" value="Submit"&gt;
        &lt;/form&gt;
    &lt;/body&gt;
&lt;/html&gt;
</code></pre>

<p><em>submit.asp</em></p>

<pre><code>&lt;%
If DATEDIFF("yyyy",now(), request.Form("Person_DateOfBirth")) &gt; 12 Then
    Response.write "You are over 12"
Else
    Response.write "You are under 12"
End if
%&gt;
</code></pre>


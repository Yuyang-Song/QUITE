# How do I get retrieve data from a form, and then save that as a variable in a java project?
[Link to question](https://stackoverflow.com/questions/39010048/how-do-i-get-retrieve-data-from-a-form-and-then-save-that-as-a-variable-in-a-ja)
**Creation Date:** 1471494692
**Score:** 0
**Tags:** java, html
## Question Body
<p>I am currently rewriting the website for my FIRST Robotics team, since it was done in GoogleSites and very quickly at that. I have previous knowledge in HTML, CSS, Java, Javascript, and SQL (MySQL and MS SQL). I have a form, and now need to get the data from that form and save it as a variable to upload to my database table.</p>

<pre><code>&lt;form method="post"&gt;
    &lt;label for="username"&gt;Username:&lt;/label&gt;
    &lt;input name="username" type="text"&gt;
    &lt;br&gt;&lt;br&gt;
    &lt;label for="password"&gt;Password:&lt;/label&gt;
    &lt;input name="password" type="text"&gt;

    &lt;input type="submit" name="submit_login" value="Submit"&gt;
&lt;/form&gt;
</code></pre>

<p>I also have this in java:</p>

<pre><code>String username = "This is a message.";
query("INSERT INTO blog (username, password) VALUES ('" + username + ", '" +
password + "');");
</code></pre>

<p>The query() method already uploads the query to MySQL and adds it to a table. So back to the question, how do I get the data from the site saved as a variable in my java project? Is it possible without php?</p>

## Answers
### Answer ID: 39010079
<p>Well you are going to <code>POST</code> the data to a servlet,</p>

<p>The servlet will have an overriden <code>doPost</code> method, where you can perform your DB 
insert.</p>

<p>Follow the <a href="http://docs.oracle.com/javaee/6/tutorial/doc/bnafd.html" rel="nofollow">servlet tutorial</a></p>


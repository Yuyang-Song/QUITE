# Can I bookmark SQL query with bind parameter?
[Link to question](https://stackoverflow.com/questions/51102910/can-i-bookmark-sql-query-with-bind-parameter)
**Creation Date:** 1530278906
**Score:** 2
**Tags:** sql, parameters, phpmyadmin
## Question Body
<p>I'm quite new to databases. I'm using phpmyadmin and I'm writing just simple SQL queries. I'm curious if I can bookmark a query with bind parameter so I could set the parameter next time again. </p>

<p>I have the following query</p>

<pre><code>SELECT startOfTest FROM `tblTest` WHERE ID = :myID
</code></pre>

<p>and I want to set <code>myID</code> every time I run the query without rewriting it in the code. </p>

<p>Is it possible?</p>

## Answers
### Answer ID: 51164615
<p>Sure, in fact there's a whole section of the manual devoted to bookmarks and <a href="https://docs.phpmyadmin.net/en/latest/bookmarks.html#variables-inside-bookmarks" rel="nofollow noreferrer">using variables in bookmarks</a>.</p>

<p>First, you'll need the <a href="https://docs.phpmyadmin.net/en/latest/setup.html#linked-tables" rel="nofollow noreferrer">phpMyAdmin Configuration Storage configured</a>. The Configuration Storage is a database that holds user-based data such as bookmarks. There's some zeroconfiguration support but I like to import the create_tables.sql file from the sql folder and configure the corresponding settings in config.inc.php. It sounds like you've already achieved that step.</p>

<p>Then, you'll want to create the bookmark with the variable inside of special  markup, so your query could become <code>SELECT startOfTest FROM `tblTest` WHERE ID=/*[VARIABLE1]*/</code>. However, this will give an error because the SQL is invalid for MySQL, so we have to build the query a little creatively. I prefer to use <code>SELECT startOfTest FROM `tblTest` WHERE 0=1 /*OR ID=[VARIABLE1]*/</code>, the 0=1 part won't match anything but is valid SQL, so your variable can be saved correctly.</p>

<p>Once you've added the bookmark, when you go to run it from the SQL tab a text box will appear where you can fill in the substitution you desire:</p>

<p><a href="https://i.sstatic.net/Ceo7D.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/Ceo7D.png" alt="Variable substitution dialog"></a></p>


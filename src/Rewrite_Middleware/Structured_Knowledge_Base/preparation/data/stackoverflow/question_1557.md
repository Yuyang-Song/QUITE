# Change (title LIKE &#39;A%&#39;) to B or C, etc (rewrite)
[Link to question](https://stackoverflow.com/questions/9593802/change-title-like-a-to-b-or-c-etc-rewrite)
**Creation Date:** 1331078171
**Score:** 3
**Tags:** php, sql, sql-like
## Question Body
<p><em>This is a rewrite of a question that was closed because it was too vague and I hadn't inserted the code correctly. Hopefully this makes more sense.</em> </p>

<p>I have a large SQL database containing 'title' and 'author'. I've set up a query using PHP that will select only titles beginning with A - (title LIKE 'A%') - on one page:</p>

<pre><code>$result = mysql_query("SELECT * FROM table WHERE (title LIKE 'A%') ORDER BY title ASC");

//fetch the data from the database
while ($row = mysql_fetch_array($result)) {
$DirPath = $row{'filename'};
//To get the innermost dir 'display just mp3'
$InnermostDir = basename(rtrim($DirPath, '/'));

echo "&lt;tr&gt;&lt;td align='justify'&gt;";
echo $row{'title'} ;
echo "&lt;/td&gt;&lt;td align='center'&gt;";
echo $row{'author'} ;
echo "&lt;/td&gt;&lt;td align='center'&gt;";
echo $row{'publisher'} ;
echo "&lt;/td&gt;&lt;td align='center'&gt;";
echo $row{'pages'} ;
echo "&lt;/td&gt;&lt;td align='center'&gt;";
echo $row{'year'} ;
echo "&lt;/td&gt;&lt;td align='center'&gt;";
echo $row{'type'} ;
echo "&lt;/td&gt;&lt;td align='center'&gt;";
echo $row{'genre'} ;
echo "&lt;/td&gt;&lt;td align='center'&gt;";
echo $row{'location'} ;
echo "&lt;/td&gt;&lt;td align='center'&gt;";
echo $row{'id'} ;
echo "&lt;/td&gt;&lt;td align='center'&gt;";
echo $row{'shortauthor'} ;
echo "&lt;/td&gt;&lt;/tr&gt;";
}
?&gt;
&lt;/table&gt;
&lt;?php
//close the connection
mysql_close($dbhandle);
?&gt;
</code></pre>

<p><a href="http://sanctuary-westminster.org/library/epa.php" rel="nofollow">http://sanctuary-westminster.org/library/epa.php</a></p>

<p>At the moment I've simply copied the page 25 time, where the only difference is that the letter changes (and the page title changes to reflect the letter), and then just use a simple a href="epb.php" to join them together. So on the epb.php page:</p>

<pre><code>$result = mysql_query("SELECT * FROM table WHERE (title LIKE 'B%') ORDER BY title ASC");
</code></pre>

<p><a href="http://sanctuary-westminster.org/library/epb.php" rel="nofollow">http://sanctuary-westminster.org/library/epb.php</a></p>

<p>This is a very long winded and unattractive approach, any changes require changing all the pages. I've tried using $letter instead of the link and have LIKE 'A%' be LIKE '$letter%' instead:</p>

<pre><code>$result = mysql_query("SELECT * FROM table WHERE (title LIKE 'row{'letter'}%') ORDER BY title ASC");
</code></pre>

<p>But that fails; it doesn't give any error messages, the query is not happening as the input value is not correct, so nothing is being returned.
Hopefully that makes better sense and apologies for before.</p>

<p>(I've also looked at ways of using a dropdown menu where the "Submit" command stores the letter chosen from the options and then it's used in the query, but when ever I look dropdown menus and SQL the only examples seem to relate to populating a menu with a table, not creating a query using one. Not sure if that would work better)</p>

## Answers
### Answer ID: 9593858
<p>Have one page, titled <code>lib.php</code> and pass it an argument, like <code>lib.php?letter=A</code></p>

<p>Change your code to:</p>

<pre><code>$result = mysql_query("SELECT * FROM table WHERE (title LIKE '" . mysql_real_escape_string($_GET['letter']) . "%') ORDER BY title ASC");
</code></pre>

<p>Now the same file, <code>lib.php</code>, can generate all the pages from before. </p>


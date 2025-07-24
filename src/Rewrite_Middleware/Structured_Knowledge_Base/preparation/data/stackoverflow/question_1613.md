# SQL Server 2005 &quot;FOR XML PATH&quot; Grouping
[Link to question](https://stackoverflow.com/questions/1443348/sql-server-2005-for-xml-path-grouping)
**Creation Date:** 1253264479
**Score:** 1
**Tags:** sql-server-2005, for-xml
## Question Body
<p>I'm trying to generate a XML document from the SQL Server 2005 database by using "FOR XML" construct.</p>

<p>There are two simple tables in the database with a one-to-many relationship:</p>

<p>1) Magazines </p>

<pre><code> | Id | Number | Name       |
 ----------------------------
 | 53 | 0001   | Magazine 1 |
 | 54 | 0002   | Magazine 2 |
 | 55 | 0003   | Magazine 3 |
</code></pre>

<p>2) Articles </p>

<pre><code> | Id |   Title   | MagazineId | Size |
 --------------------------------------
 | 1  | Article 1 |        53  | 1205 |
 | 2  | Article 2 |        53  | 817  |
 | 3  | Article 3 |        54  | 1570 |
 | 4  | Article 4 |        54  | 2510 |
 | 5  | Article 5 |        55  | 910  |
</code></pre>

<p>Let's assume I have to find all magazines that have an article with size greater than 1000 
and to produce the following xml:</p>

<pre><code>&lt;Magazines&gt;
    &lt;Magazine Id="53"&gt;
      &lt;Number&gt;0001&lt;/Number&gt;
      &lt;Articles&gt;
        &lt;Article Id="1"&gt;
           &lt;Title&gt;Article 1&lt;/Title&gt;
           &lt;Size&gt;1205&lt;/Size&gt;
        &lt;/Article&gt;
      &lt;/Articles&gt;
    &lt;/Magazine&gt;
    &lt;Magazine Id="54"&gt;
      &lt;Number&gt;0002&lt;/Number&gt;
      &lt;Articles&gt;
        &lt;Article Id="3"&gt;
          &lt;Title&gt;Article 3&lt;/Title&gt;
          &lt;Size&gt;1570&lt;/Size&gt;
        &lt;/Article&gt;
        &lt;Article Id="4"&gt;
          &lt;Title&gt;Article 4&lt;/Title&gt;
          &lt;Size&gt;2510&lt;/Size&gt;
        &lt;/Article&gt;
      &lt;/Articles&gt;
    &lt;/Magazine&gt;
&lt;/Magazines&gt;
</code></pre>

<p>I'm trying to produce such xml by using a "PATH" mode:</p>

<pre><code>SELECT Magazines.Id AS "@Id",
       Magazines.Number AS "Number",
       Articles.Id AS "Articles/Article/@Id",
       Articles.Title AS "Articles/Article/Title",
       Articles.Size AS "Articles/Article/Size"
FROM Magazines INNER JOIN Articles ON Magazines.Id = Articles.MagazineId
WHERE Articles.Size &gt; 1000
FOR XML PATH('Magazine'), ROOT('Magazines'), TYPE
</code></pre>

<p>It will produce the following xml:</p>

<pre><code>&lt;Magazines&gt;
  &lt;Magazine Id="53"&gt;
    &lt;Number&gt;0001&lt;/Number&gt;
    &lt;Articles&gt;
      &lt;Article Id="1"&gt;
        &lt;Title&gt;Article 1&lt;/Title&gt;
        &lt;Size&gt;1205&lt;/Size&gt;
      &lt;/Article&gt;
    &lt;/Articles&gt;
  &lt;/Magazine&gt;
  &lt;Magazine Id="54"&gt;
    &lt;Number&gt;0002&lt;/Number&gt;
    &lt;Articles&gt;
      &lt;Article Id="3"&gt;
        &lt;Title&gt;Article 3&lt;/Title&gt;
        &lt;Size&gt;1570&lt;/Size&gt;
      &lt;/Article&gt;
    &lt;/Articles&gt;
  &lt;/Magazine&gt;
  &lt;Magazine Id="54"&gt;
    &lt;Number&gt;0002&lt;/Number&gt;
    &lt;Articles&gt;
      &lt;Article Id="4"&gt;
        &lt;Title&gt;Article 4&lt;/Title&gt;
        &lt;Size&gt;2510&lt;/Size&gt;
      &lt;/Article&gt;
    &lt;/Articles&gt;
  &lt;/Magazine&gt;
&lt;/Magazines&gt;
</code></pre>

<p>So there are two elements for the Magazine with Id="54" (one for each article) and this is the problem.</p>

<p>I can rewrite the query using a subquery like this:</p>

<pre><code>SELECT M.Id AS "@Id",
       M.Number AS "Number",
    (SELECT Articles.Id AS "@Id",
               Articles.Title AS "Title",
               Articles.Size AS "Size"
  FROM Articles
  WHERE Articles.MagazineId = M.Id
  FOR XML PATH('Article'), ROOT('Articles'), TYPE
    )
FROM Magazines AS M 
FOR XML PATH('Magazine'), ROOT('Magazines'), TYPE
</code></pre>

<p>And this produce the following xml:</p>

<pre><code>&lt;Magazines&gt;
  &lt;Magazine Id="53"&gt;
    &lt;Number&gt;0001&lt;/Number&gt;
    &lt;Articles&gt;
      &lt;Article Id="1"&gt;
        &lt;Title&gt;Article 1&lt;/Title&gt;
        &lt;Size&gt;1205&lt;/Size&gt;
      &lt;/Article&gt;
      &lt;Article Id="2"&gt;
        &lt;Title&gt;Article 2&lt;/Title&gt;
        &lt;Size&gt;817&lt;/Size&gt;
      &lt;/Article&gt;
    &lt;/Articles&gt;
  &lt;/Magazine&gt;
  &lt;Magazine Id="54"&gt;
    &lt;Number&gt;0002&lt;/Number&gt;
    &lt;Articles&gt;
      &lt;Article Id="3"&gt;
        &lt;Title&gt;Article 3&lt;/Title&gt;
        &lt;Size&gt;1570&lt;/Size&gt;
      &lt;/Article&gt;
      &lt;Article Id="4"&gt;
        &lt;Title&gt;Article 4&lt;/Title&gt;
        &lt;Size&gt;2510&lt;/Size&gt;
      &lt;/Article&gt;
    &lt;/Articles&gt;
  &lt;/Magazine&gt;
  &lt;Magazine Id="55"&gt;
    &lt;Number&gt;0003&lt;/Number&gt;
    &lt;Articles&gt;
      &lt;Article Id="5"&gt;
        &lt;Title&gt;Article 5&lt;/Title&gt;
        &lt;Size&gt;910&lt;/Size&gt;
      &lt;/Article&gt;
    &lt;/Articles&gt;
  &lt;/Magazine&gt;
&lt;/Magazines&gt;
</code></pre>

<p>But by using a subquery I can not filter magazines by articles columns (without complex additional queries).</p>

<p>The "FOR XML AUTO" mode is not suitable, because it is very simple and does not support some "PATH" features (like attributes using @, ROOT, etc..)</p>

<p>So, Is there any possibility in "PATH" mode to group inner table data like in "AUTO" mode?</p>

<p>Thank you!</p>

## Answers
### Answer ID: 1743670
<p>Use FOR XML explicit. Is longest code to write but disappear the performance issues provocate by sub queries.</p>

### Answer ID: 1443806
<p>Well, you can get one step closer by specifying the "size > 1000" inside your subquery:</p>

<pre><code>SELECT M.Id AS "@Id",
       M.Number AS "Number",
    (SELECT Articles.Id AS "@Id",
               Articles.Title AS "Title",
               Articles.Size AS "Size"
     FROM Articles
     WHERE Articles.MagazineId = M.Id
           AND Articles.Size &gt; 1000
     FOR XML PATH('Article'), ROOT('Articles'), TYPE
    )
FROM Magazines AS M 
FOR XML PATH('Magazine'), ROOT('Magazines'), TYPE
</code></pre>

<p>What you're missing now is the fact you'll still get magazines that have no articles with a size > 1000. You can eliminate those something like this:</p>

<pre><code>SELECT M.Id AS "@Id",
       M.Number AS "Number",
    (SELECT Articles.Id AS "@Id",
               Articles.Title AS "Title",
               Articles.Size AS "Size"
      FROM Articles
      WHERE Articles.MagazineId = M.Id
            AND Articles.Size &gt; 1000
      FOR XML PATH('Article'), ROOT('Articles'), TYPE
    )
FROM Magazines AS M 
WHERE EXISTS(SELECT * FROM Articles 
             WHERE Articles.MagazineId = M.Id 
               AND Articles.Size &gt; 1000)
FOR XML PATH('Magazine'), ROOT('Magazines'), TYPE
</code></pre>

<p>(untested, I don't have a SQL server at hand right now).</p>

<p>Does that work for you? Does it give you the magazines and articles you're looking for?</p>

<p>Marc</p>


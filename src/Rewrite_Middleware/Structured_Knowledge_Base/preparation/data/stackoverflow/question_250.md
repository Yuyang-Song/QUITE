# SQL - retrieval query for specific string
[Link to question](https://stackoverflow.com/questions/18074017/sql-retrieval-query-for-specific-string)
**Creation Date:** 1375773827
**Score:** 0
**Tags:** sql
## Question Body
<p>I am making a small database at the moment (less than 50 entries) and I am having trouble with a query. My query at the moment is </p>

<pre><code>SELECT  Name
FROM Customers 
WHERE Name LIKE '%Adam%'
</code></pre>

<p>The names are in the format of "Adam West".</p>

<p>The query works fine in retrieving all the people with "Adam" in their name but I would like to only retrieve the first name, not the last name. I don't want to split the columns up but would like to know how to rewrite my query to account for this.</p>

## Answers
### Answer ID: 18074500
<p>if you are storing name with space as separator example "Adam abcd" where 'Adam' is firstname and 'abcd' as lastname then following will work</p>

<pre><code>SELECT     Expr1
FROM         (SELECT     LEFT(Name, CHARINDEX(' ', Name, 1)) AS Expr1
                       FROM          Customers) AS derivedtbl_1
WHERE     (Expr1 LIKE 'Adm%')
</code></pre>

<p>for more details read this article <a href="http://suite101.com/article/sql-functions-leftrightsubstrlengthcharindex-a209089" rel="nofollow">http://suite101.com/article/sql-functions-leftrightsubstrlengthcharindex-a209089</a></p>

### Answer ID: 18074208
<p>You should indeed "split" your columns and normalize your tables to avoid having to use complicated string functions to search for a lastname or firstname or what ever you need to look for. What about if someone entered lastname first and then firstname? Or just a nickname?</p>

<p>That said, check the use of <code>LIKE</code> on <a href="http://technet.microsoft.com/es-es/library/ms179859.aspx" rel="nofollow">Microsoft technet site</a>. The following query should be helpful on you case:</p>

<pre><code>SELECT Name
  FROM Customers
 WHERE Name LIKE 'Adam%'
</code></pre>

### Answer ID: 18074159
<p>Try this</p>

<p>{SELECT  Name
FROM Customers 
WHERE SUBSTRING(Name,1,CHARINDEX(' ',Name)-1) LIKE '%Adam%'
}</p>

<p>I assumed the first name and last name is saparated by space and i took the firstname out</p>

<p>Using SUBSTRING(Name,1,CHARINDEX(' ',Name)-1)
and compared how you wanted. if your have something else saparating first name and last name change space in charindex with the saparater.</p>

<p>Please let me know if any other help needed.</p>

<p>Regards</p>

<p>Ashutosh</p>

### Answer ID: 18074098
<p>If the name of your customers starts with first name (like <em>Adam West</em>) you can use</p>

<pre><code>select Name
from Customers
where Name like 'Adam %'
</code></pre>

<p>Otherwise, if the format of the name is <code>&lt;last name&gt; &lt;first name&gt;</code> you can use</p>

<pre><code>select Name
from Customers
where Name like '% Adam' 
</code></pre>

### Answer ID: 18074058
<p>SELECT  Name
FROM Customers 
WHERE Name LIKE 'Adam%'</p>


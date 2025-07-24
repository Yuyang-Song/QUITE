# ColdFusion DateDiff - Is there a better way?
[Link to question](https://stackoverflow.com/questions/30877354/coldfusion-datediff-is-there-a-better-way)
**Creation Date:** 1434485865
**Score:** 2
**Tags:** mysql, coldfusion, datediff, simplify
## Question Body
<p>I simply want to combine the total years of service from various members of my team.  The below script works fine, however, the hire date for each member does not pull from a database.  Which means I have to hard code each persons hiredate and then do a DateDiff on them.  With a team of 28 members that would cause a code management nightmare.</p>

<p>My main goal is to make the code simpler and more efficient, especially when managing 28 team members.  If part of the path requires adding the user's hiredate to a database; I can do that.  I just see the code below needing a rewrite, I just don't know the best method.</p>

<p>Is there a better way?  </p>

<pre><code>&lt;cfscript&gt;
  REQUEST.rightnow = Now();
  dateBob = DateDiff("yyyy", "1996 02 01", REQUEST.rightnow);
  dateSam = DateDiff("yyyy", "1996 08 01", REQUEST.rightnow);
  dateJoe = DateDiff("yyyy", "2004 12 01", REQUEST.rightnow);
  dateJohn = DateDiff("yyyy", "2001 01 01", REQUEST.rightnow);
  combinedDate = (dateBob + dateSam + dateJoe + dateJohn);
&lt;/cfscript&gt;
&lt;cfoutput&gt;
  #combinedDate# total years&lt;br&gt;
  #dateBob# years&lt;br&gt;
  #dateSam# years&lt;br&gt;
  #dateJoe# years&lt;br&gt;
  #dateJohn# years&lt;br&gt;
&lt;/cfoutput&gt;
</code></pre>

<p>--- EDIT ---</p>

<p>Per Matt's suggestion as a database query; something like this?</p>

<pre><code>SELECT hire_date,
        ROUND((DATEDIFF(NOW(),hire_date)) / 365) AS dateDiff
FROM members
WHERE hire_date IS NOT NULL
</code></pre>

<p>--- EDIT 2 ---</p>

<p>I just realised I forgot to add SUM() of all the "dateDiff".  If anyone uses this SQL you will have to hand it off to ColdFusion, I suppose.  Unless I overlooked a way to do it in SQL?</p>

<p>--- EDIT 3 ---</p>

<p>Per Leigh's comments of encouragement; I found a better way.  The TIMESTAMPDIFF() MySQL function adds a <em>unit</em> variable that can be day, month, year, etc.  This allowed me to remove the / 365 and the ROUND().  Which in turn allowed me to use SUM() and not get a syntax error from MySQL.  I also renamed my alias from dateDiff to just Dif because I wanted to avoid confusion with DATEDIFF().</p>

<p>See below. :D</p>

<pre><code>SELECT hire_date,
        SUM(TIMESTAMPDIFF(YEAR,hire_date,NOW())) AS Dif
FROM members
WHERE hire_date IS NOT NULL
</code></pre>

## Answers
### Answer ID: 30895172
<p>The solution to improving the code posted for ColdFusion was actually replacing it.   By adding the hire_dates of each member to an existing MySQL database and writing the query below; I no longer needed all of the ColdFusion code in my original post.</p>

<pre><code>SELECT SUM(TIMESTAMPDIFF(YEAR,hire_date,NOW())) AS Dif
FROM members
WHERE hire_date IS NOT NULL
</code></pre>


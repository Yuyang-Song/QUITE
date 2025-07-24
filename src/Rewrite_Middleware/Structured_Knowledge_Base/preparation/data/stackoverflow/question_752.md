# SQL Like Statement is showing all results
[Link to question](https://stackoverflow.com/questions/40622101/sql-like-statement-is-showing-all-results)
**Creation Date:** 1479255968
**Score:** 1
**Tags:** mysql
## Question Body
<p>I have used LIKE statements before and have been spending ages rewriting the statement and not sure what I have done wrong. When the query is ran, it displays all records in the database when it should be showing a more narrow list. </p>

<p>The reason for using a LIKE statement is to make my advanced search facility more efficient by allow part of a "property name".   </p>

<p><strong>SQL Statement:</strong></p>

<pre><code>SELECT
    *
FROM
    properties
WHERE
    PropertyName LIKE '%$PropertyName%'
    OR PropertyLocation LIKE '%$PropertyLocation%'
    OR PropertyType LIKE '%$PropertyType%'
    OR PropertyBeds='$PropertyBeds'
    OR PropertyRate &gt;= '$PropertyRate1'
    AND PropertyRate &lt;= '$PropertyRate2'
</code></pre>

<p><strong>Please note:</strong> The statement does work without using like and wildcards. </p>

## Answers
### Answer ID: 40622123
<p>Your conditions are:</p>

<pre><code>WHERE PropertyName LIKE '%$PropertyName%' or
      PropertyLocation LIKE '%$PropertyLocation%' or
      PropertyType LIKE '%$PropertyType%' or
      PropertyBeds = '$PropertyBeds' or
      PropertyRate &gt;= '$PropertyRate1' and PropertyRate &lt;= '$PropertyRate2' 
</code></pre>

<p>If <code>PropertyName</code>, <code>PropertyLocation</code>, or <code>PropertyType</code> are empty strings, then you will return all the rows.  That is my first guess on what is happening.</p>

<p>Perhaps you want <code>AND</code> as a connector rather than <code>OR</code>.</p>


# How to list duplicate entries in database
[Link to question](https://stackoverflow.com/questions/4453548/how-to-list-duplicate-entries-in-database)
**Creation Date:** 1292438082
**Score:** 0
**Tags:** php, mysql
## Question Body
<p>how can i write a query to list duplicate entries in a database from the same category. The duplicates have the same value in the "name" column. I need to list only the duplicates in the same category so I can then delete the duplicate.</p>

<p>I am using this example from a search   </p>

<pre><code> SELECT email FROM tableName GROUP BY email HAVING count(email) &gt; 1
</code></pre>

<p>That works for getting duplicates but it gets all duplicates, how can i rewrite it to get the duplicates from the same categories.
In the above example, if i have an email that exists in the cat 1 and cat 4, it will be shown as duplicate, which is not the case. It should only list duplicates if the email exists twice or more in cat 1, or twice and more in cat 4 and so on.</p>

<p>Thanks.</p>

## Answers
### Answer ID: 4453613
<p>You can add more than one column to a group by.  I.E.</p>

<pre><code>SELECT email, category from tableName GROUP BY email, category HAVING count(email) &gt; 1
</code></pre>

<p>That will show the email and category only where the email and category are both duplicate (I.E. same email twice with same category).</p>

### Answer ID: 4453595
<p>Add the category to the group by.</p>

<pre><code>SELECT email FROM tableName GROUP BY email, category HAVING count(email) &gt; 1
</code></pre>

<p>The only thing wrong with this is you won't be able to tell which category the duplicate is in unless you <code>SELECT</code> on it as well.</p>


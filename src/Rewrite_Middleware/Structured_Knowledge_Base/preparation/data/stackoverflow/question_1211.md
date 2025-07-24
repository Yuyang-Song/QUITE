# How to use bind variables for date literals?
[Link to question](https://stackoverflow.com/questions/63780647/how-to-use-bind-variables-for-date-literals)
**Creation Date:** 1599493282
**Score:** 2
**Tags:** sql, oracle-database
## Question Body
<p>Consider the following SQL</p>
<pre><code>SELECT * FROM employee WHERE dob = DATE '1980-05-15'
</code></pre>
<p>I need to rewrite the query to get rid of the hard coded values and use bind variables instead. So, my rewritten query looks like this</p>
<pre><code>SELECT * FROM employee WHERE dob = DATE :dateOfBirth
</code></pre>
<p>However, the query doesn't work. I've tried all possible formats (1980-05-15, 15-MAY-80, 15-MAY-1980) for :dateOfBirth variable, without any luck. I always get <em>ORA-00936: missing expression</em> error.</p>
<p><strong>Note 1:</strong> I'm aware of to_date() function that can solve my issue, but I can't use that because the query originates from a different system on which I don't have any control over.</p>
<p><strong>Note 2:</strong> DD-MON-RR is the nls_date_format in my database as specified in nls_session_parameters &amp; nls_database_parameters</p>

## Answers
### Answer ID: 63780737
<p>You can't, you need to <code>to_date</code> it:</p>
<pre><code>SELECT * FROM employee WHERE dob = to_date ( :dateOfBirth, '&lt;fmt&gt;' );
</code></pre>


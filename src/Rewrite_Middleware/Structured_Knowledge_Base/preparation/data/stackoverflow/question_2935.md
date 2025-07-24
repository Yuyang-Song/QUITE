# ERROR: could not write block 37583345 of temporary file: No space left on device
[Link to question](https://stackoverflow.com/questions/59278180/error-could-not-write-block-37583345-of-temporary-file-no-space-left-on-device)
**Creation Date:** 1576032291
**Score:** 0
**Tags:** postgresql, postgresql-12
## Question Body
<p>I want an output like this:</p>

<pre><code>obid     | sid_count
1        |  3
2        |  2
3        |  4
</code></pre>

<p>The obid is on custdata table and sid_count is get from identifier table.</p>

<p>The sample data is:</p>

<pre><code>custdata
obid
1
2
3

identifier
obid | type
1    | SID
1    | SID
1    | XID
1    | SID
2    | SID
2    | SID
3    | SID
3    | SID
3    | XID
3    | SID
3    | SID
</code></pre>

<p>I try to run this query:</p>

<pre><code>select custdata.obid,
count (identifier.obid) filter (where identifier.type = 'SID') as sid_count
from myschema.custdata, myschema.identifier group by custdata.obid
</code></pre>

<p>it took about an hour but got an error:</p>

<pre><code>[53100] ERROR: could not write block 37583345 of temporary file: No space left on device
</code></pre>

<p>The custdata is about 65 million records.
The identifier is about 250 million records.</p>

<p>How to overcome this problem? Why the database need to write to disk? or do i need to rewrite my query? because i can't add more space to the disk.</p>

<p>Thanks.</p>

## Answers
### Answer ID: 59279446
<p>The problem is that you inadvertently wrote a cross join:</p>

<pre><code>from myschema.custdata, myschema.identifier
</code></pre>

<p>That is, each of the 250 million rows of the one table is joined with each of the 65 million rows of the other table, resulting in 16.25 quadrillion result rows. Your data directory does not seem to have room to cache the temporary required to complete the query, so you are running out of disk space there.</p>

<p>As a solution, add a join condition.</p>

<p>Take the opportunity and learn to <strong>never again</strong> write joins like this. Always use the standard syntax:</p>

<pre><code>FROM a JOIN b ON &lt;condition&gt;
</code></pre>

<p>That way you cannot forget the join condition, unless you explicitly specify</p>

<pre><code>FROM a CROSS JOIN b
</code></pre>

<p>which will be way more obvious.</p>


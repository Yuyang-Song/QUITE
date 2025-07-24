# Add an MD5 index to a table
[Link to question](https://stackoverflow.com/questions/52167058/add-an-md5-index-to-a-table)
**Creation Date:** 1536066378
**Score:** 1
**Tags:** ruby-on-rails, postgresql, activerecord
## Question Body
<p>I have a table in a Postgresql database with a column containing large texts.
I ran into this problem:</p>

<pre><code>HINT:  Values larger than 1/3 of a buffer page cannot be indexed.
Consider a function index of an MD5 hash of the value, or use full text indexing.
</code></pre>

<p>So I want to add a MD5 index to this table. 
I found how to do so in PG, but not in with ActiveRecord. Any idea on how to do this in a migration? Will my queries use this index by default or do I need to rewrite a bunch of them ?</p>


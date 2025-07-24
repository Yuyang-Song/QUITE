# What does &quot;Using sort_union&quot; mean?
[Link to question](https://stackoverflow.com/questions/6463695/what-does-using-sort-union-mean)
**Creation Date:** 1308892494
**Score:** 4
**Tags:** mysql, sql-execution-plan
## Question Body
<p>(Not sure is this has been discussed before ...)</p>

<p>When building SQL for category</p>

<p>example category data:</p>

<pre><code>ID | NAME
--------------------------
1  | hardware
2  | hardware : notebooks
3  | hardware : phones
4  | hardware : desktops
5  | review
6  | review : photo gallery
</code></pre>

<p><code>hardware</code> will be the parent category for <code>hardware : *</code></p>

<p>When I considering building api to query database</p>

<pre><code>desc select * from category 
where id=1 or 
name like concat((select name from category where id in(1)), '_%');
</code></pre>

<p>the above return (in the execution plan)</p>

<pre><code>Using sort_union(PRIMARY,some_index); Using where
</code></pre>

<p>What is the <code>sort_union</code> means ?<br>
Good ? Bad? To be avoid ?</p>

<hr>

<p>(understand I could rewrite the entire query into a more optimize way,<br>
but there are some constraints for me to re-build the entire api)</p>

<hr>

<p>mysql version 5.1</p>

## Answers
### Answer ID: 6463733
<p>sort_union is used when you have a where clause in which you are OR'ing two or more, for which MySQL thinks it's better than using index_merge.</p>

<p>For more information, <a href="http://dev.mysql.com/doc/refman/5.5/en/index-merge-sort-union.html" rel="noreferrer">see the MySQL docs</a></p>

<p>In short, it's not bad (imho); since it will fetch the rows from both indexes first, before sort-unioning them.</p>


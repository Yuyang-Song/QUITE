# Processing large amount of data from PostgreSQL
[Link to question](https://stackoverflow.com/questions/54874407/processing-large-amount-of-data-from-postgresql)
**Creation Date:** 1551127539
**Score:** 2
**Tags:** java, postgresql, hibernate, jpa, jdbc
## Question Body
<p>I am looking for a way how to process a large amount of data that are loaded from the database in a reasonable time.</p>

<p>The problem I am facing is that I have to read all the data from the database (currently around 30M of rows) and then process them in Java. The processing itself is not the problem but fetching the data from the database is. The fetching generally takes from 1-2 minutes. However, I need it to be much faster than that. I am loading the data from db straight to DTO using following query:</p>

<pre><code>select id, id_post, id_comment, col_a, col_b from post_comment
</code></pre>

<p>Where <code>id</code> is primary key, <code>id_post</code> and <code>id_comment</code> are foreign keys to respective tables and <code>col_a</code> and <code>col_b</code> are columns of small int data types. The columns with foreign keys have indexes.
The tools I am using for the job currently are Java, Spring Boot, Hibernate and PostgreSQL.</p>

<p>So far the only options that came to my mind were</p>

<ol>
<li>Ditch hibernate for this query and try to use plain jdbc connection hoping that it will be faster.</li>
<li>Completely rewrite the processing algorithm from Java to SQL procedure.</li>
</ol>

<p>Did I miss something or these are my only options? I am open to any ideas.
Note that I only need to read the data, not change them in any way.</p>

<p>EDIT: The explain analyze of the used query</p>

<pre><code>"Seq Scan on post_comment (cost=0.00..397818.16 rows=21809216 width=28) (actual time=0.044..6287.066 rows=21812469 loops=1), Planning Time: 0.124 ms, Execution Time: 8237.090 ms"
</code></pre>

## Answers
### Answer ID: 54875946
<p>Since you asked for ideas, I have seen this problem being resolved in below options depending on how it fits in your environment:
1) First try with JDBC and Java, simple code and you can do a test run on your database and data to see if this improvement is enough. You will here need to compromise on the other benefits of Hibernate.
2) In point 1, use Multi-threading with multiple connections pulling data to one queue and then you can use that queue to process further or print as you need. you may consider Kafka also.
3) If data is going to further keep on increasing you can consider Spark as the latest technology which can make it all in memory and will be much more faster.</p>

<p>These are some of the options, please like if these ideas help you anywhere.</p>

### Answer ID: 54875847
<p>If I was in your shoes I would definitely bypass hibernate and go directly to JDBC for this query. Hibernate is not made for dealing with large result sets, and it represents an additional overhead for benefits that are not applicable to cases like this one. </p>

<p>When you use JDBC, do not forget to set autocommit to false and set some large fetch size (of the order of thousands) or else postgres will first fetch all 21 million rows into memory before starting to yield them to you.  (See <a href="https://stackoverflow.com/a/10959288/773113">https://stackoverflow.com/a/10959288/773113</a>)</p>

### Answer ID: 54874810
<p>Do you need to process all rows at once, or can you process them one at a time?</p>

<p>If you can process them one at a time, you should try using a scrollable result set.</p>

<pre><code>org.hibernate.Query query = ...;
query.setReadOnly(true);
ScrollableResults sr = query.scroll(ScrollMode.FORWARD_ONLY);

while(sr.next())
{
    MyClass myObject = (MyClass)sr.get()[0];
    ... process row for myObject ... 
}
</code></pre>

<p>This will <em>still</em> remember every object in the entity manager, and so will get progressively slower and slower.  To avoid that issue, you might detach the object from the entity manager after you're done.  This can only be done if the objects are not modified.  If they are modified, the changes will NOT be persisted.</p>

<pre><code>org.hibernate.Query query = ...;
query.setReadOnly(true);
ScrollableResults sr = query.scroll(ScrollMode.FORWARD_ONLY);

while(sr.next())
{
    MyClass myObject = (MyClass)sr.get()[0];
    ... process row for myObject ... 
    entityManager.detach(myObject);
}
</code></pre>

### Answer ID: 54874451
<p>Why do you 30M keep in memory ??
it's better to rewrite it to pure sql and use pagination based on id</p>

<p>you will be sent 5 as the id of the last comment and you will issue </p>

<pre><code>select id, id_post, id_comment, col_a, col_b from post_comment where id &gt; 5 limit 20
</code></pre>

<p>if you need to update the entire table then you need to put the task in the cron but also there to process it in parts
the memory of the road and downloading 30M is very expensive - you need to process parts <strong>0-20 20-n n+20</strong></p>


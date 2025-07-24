# How to store big data?
[Link to question](https://stackoverflow.com/questions/18660650/how-to-store-big-data)
**Creation Date:** 1378479160
**Score:** -2
**Tags:** sqlite, storage, scalability, bigdata
## Question Body
<p>Suppose we have a web service that aggregates 20 000 users, and each one of them is linked to 300 unique user data entities containing whatever. Here's naive approach on how to design an example relational database that would be able to store above data:</p>

<ol>
<li>Create table for users.</li>
<li>Create table for user data.</li>
</ol>

<p>And thus, user data table contains 6 000 000 rows.</p>

<p>Querying tables that have millions of rows is slow, especially since we have to deal with hierarchical data and do some uncommon computations much different from <code>SELECT * FROM userdata</code>. At any given point, we only need specific user's data, not the whole thing - getting it is fast - but we have to do weird stuff with it later. Multiple times.</p>

<p>I'd like our web service to be fast, so I thought of following approaches:</p>

<ol>
<li>Optimize the hell out of queries, do a lot of caching etc. This is nice, but these are just temporary workarounds. When database grows even further, these will cease to work.</li>
<li>Rewriting our model layer to use NoSQL technology. This is not possible due to lack of relational database features and even if we wanted this approach, early tests made some functionalities even slower than they already were.</li>
<li><p>Implement some kind of scalability. (You hear about cloud computing a lot nowadays.) This is the most wanted option.</p>

<ol>
<li>Implement some manual solution. For example, I could store all the users with names beginning with letter "A..M" on server 1, while all other users would belong to server 2. The problem with this approach is that I have to redesign our architecture quite a lot and I'd like to avoid that.</li>
<li>Ideally, I'd have some kind of transparent solution that would allow me to query seemingly uniform database server with no changes to code whatsoever. The database server would scatter its table data on many workers in a smart way (much like database optimizers), thus effectively speeding everything up. (Is this even possible?) </li>
</ol>

<p>In both cases, achieving interoperability seems like a lot of trouble...</p></li>
<li>Switching from SQLite to Postgres or Oracle solution. This isn't going to be cheap, so I'd like some kind of confirmation before doing this.</li>
</ol>

<p>What are my options? I want all my <code>SELECT</code>s and <code>JOIN</code>s with indexed data to be real-time, but the bigger the <code>userdata</code> is, the more expensive queries get.</p>

## Answers
### Answer ID: 18684904
<p>I don't think that you should use NoSQL by default if you have such amount of data. Which kind of issue are you expecting that it will solve?</p>

<p>IMHO this depends on your queries. You haven't mentioned some kind of massive writing so SQL is still appropriate so far.</p>

<p>It sounds like you want to perform queries using <code>JOIN</code>s. This could be slow on very large data even with appropriate indexes. What you can do is to lower your level of decomposition and just duplicate a data (so they all are in one database row and are fetched together from hard drive). If you concern latency, avoid joining is good approach. But it still does not eliminates SQL as you can duplicate data even in SQL.</p>

<p>Significant for your decision making should be structure of your queries. Do you want to <code>SELECT</code> only few fields within your queries (SQL) or do you want to <em>always</em> get the whole document (e.g. Mongo &amp; Json). </p>

<p>The second significant criteria is scalability as NoSQL often relaxes usual SQL things (like eventual consistency) so it can provide better results using scaling out.</p>


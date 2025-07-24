# NHibernate MultiQuery for Java
[Link to question](https://stackoverflow.com/questions/3229741/nhibernate-multiquery-for-java)
**Creation Date:** 1278948429
**Score:** 1
**Tags:** java, hibernate
## Question Body
<p>NHibernate (for .Net) has an interface called IMultiQuery which you can instantiate an implementation for using ISession.CreateMultiQuery(). A multi-query allows one to run multiple hql statements in a single batch. I can't seem to find an equivalent feature in Hibernate (for Java).</p>

<p>Multi-query would be perfect for the java application I'm working on right now. It has about 10 HQL select queries running inside a tight loop. Load testing shows that it's about 50% too slow (or said in another way, it takes twice as long as required). My analysis says that almost all of the time is spent on network latency between the app server and the database. I can definitely rewrite the code to avoid the tight loop, but that was the simplest design and it's already been QAed for correctness. </p>

<p>So, if I can somehow shoot off all 10 HQL queries in a single batch, that should give more than enough of a performance boost without resorting to more drastic and bug-prone measures. Is there any way to do that with Hibernate in Java?</p>

## Answers
### Answer ID: 3230077
<p>I'm not aware of a Java equivalent of the Multi Query and I think this feature is specific to the .net version (because it is database specific). From the NHibernate documentation:</p>

<blockquote>
  <h3><a href="http://nhibernate.info/doc/nh/en/index.html#performance-multi-query" rel="nofollow noreferrer">17.7. Multi Query</a></h3>
  
  <p>Multi query is executed by
  concatenating the queries and sending
  the query to the database as a single
  string. This means that the database
  should support returning several
  result sets in a single query. At the
  moment this functionality is only
  enabled for Microsoft SQL Server and
  SQLite.</p>
</blockquote>


# Elegant ways to handle database views on hibernate entities?
[Link to question](https://stackoverflow.com/questions/901537/elegant-ways-to-handle-database-views-on-hibernate-entities)
**Creation Date:** 1243085295
**Score:** 26
**Tags:** java, database, hibernate
## Question Body
<p>One of the main reasons I use Hibernate is that it provides the flexibility to switch to another database without having to rewrite any code. </p>

<p>But until now I did not figure out a good way to define additional views on the tables to which my hibernate entities are matched; I am still using simple SQL scripts for that. Is there a more elegant way to define views on tables managed by hibernate? </p>

<p>Ideally I would like to use HQL or another generic method to do the job, so that I don't have to worry about my SQL scripts being incompatible with other kinds of databases.</p>

<p>If there's a way to do that, a second issue would then be to get 'synthetic' read-only instances from these views, which should make it much easier to feed the aggregated data into a UI.</p>

<p><strong>EDIT:</strong></p>

<p>It seems as if I didn't make the problem clear enough, so here's what i am trying to do: I want to write code that is independent of the used database. Since I use hibernate, I would just have to change the dialect configuration file and could then use another DBMS. </p>

<p>Question: how to create <em>views</em> on my hibernate entities <em>without</em> relying on a specific SQL dialect (to keep everything portable), or even HQL? And if that's possible, can I use HQL to also query these views, i.e. to create read-only aggregate entities? Is there any additional hibernate plug-in to help me with that? Haven't found anything so far... :-/</p>

## Answers
### Answer ID: 1529855
<p>Had the same problem and found the following solution in the hibernate doucmentation:</p>

<blockquote>
  <p>There is no difference between a view
  and a base table for a Hibernate
  mapping. This is transparent at the
  database level, although some DBMS do
  not support views properly, especially
  with updates. Sometimes you want to
  use a view, but you cannot create one
  in the database (i.e. with a legacy
  schema). In this case, you can map an
  immutable and read-only entity to a
  given SQL subselect expression:</p>
</blockquote>

<pre><code>&lt;class name="Summary"&gt;
    &lt;subselect&gt;
        select item.name, max(bid.amount), count(*)
        from item
        join bid on bid.item_id = item.id
        group by item.name
    &lt;/subselect&gt;
    &lt;synchronize table="item"/&gt;
    &lt;synchronize table="bid"/&gt;
    &lt;id name="name"/&gt;
    ...
&lt;/class&gt;
</code></pre>

<p><a href="https://docs.jboss.org/hibernate/stable/core/manual/en-US/html_single/#mapping-declaration" rel="nofollow noreferrer">https://docs.jboss.org/hibernate/stable/core/manual/en-US/html_single/#mapping-declaration</a></p>

### Answer ID: 908074
<p>Can you declare the views directly inside the database?
Then you can just select directly from the views.
Have a look at <a href="http://docs.jboss.org/hibernate/stable/core/reference/en/html/objectstate-querying.html#objectstate-querying-nativesql" rel="nofollow noreferrer">chapter 10.4.4 of the Hibernate manual</a></p>

<p>That should allow you to SELECT from the database view and get Hibernate to automatically hydrate the data into your entities.</p>

<p>Of course, a view doesn't take any parameters.
Hibernate 3 is supposed to support stored procedures, but I've used that.</p>

### Answer ID: 913770
<p>Hibernate will not automatically create the views for you, as each dialect supports only a limited subset of the data-definition language (DDL) of the underlying database. Basically, it supports enough DDL to generate a working schema, but not enough to handle creation of "extra" objects like views.</p>

<p>All is not lost, though. Hibernate does give you the ability to create (and drop) additional database objects yourself in the XML mapping files, and those objects can be scoped to a particular dialect. For example, I could have a mapping like this:</p>

<pre><code>&lt;hibernate-mapping&gt;
  &lt;class name='com.mycompany.myproduct.Customer' table='tbl_customer'&gt;
    &lt;id name='id' column='customer_id'&gt;
      &lt;generator class='native'/&gt;
    &lt;/id&gt;
    &lt;property name='name' length='50' unique='true' not-null='true' /&gt;
  &lt;/class&gt;

  &lt;database-object&gt;
    &lt;create&gt;create or replace view read_only_cust...&lt;/create&gt;
    &lt;drop&gt;drop view read_only_cust&lt;/drop&gt;
    &lt;dialect-scope name='org.hibernate.dialect.Oracle9Dialect' /&gt;
  &lt;/database-object&gt;
&lt;/hibernate-mapping&gt;
</code></pre>

<p>You're free to create whatever additional views you want by adding more "database-object" sections. You have to write the SQL (DDL) yourself for each database you want to support, but since they're scoped to the dialect, Hibernate will only execute the SQL for the dialect chosen at schema export time.</p>

### Answer ID: 912005
<p>What do you mean by "create view"?  I know what it means from a pure DB context - but that is not what you mean - right?  </p>

<p>You can either map new Java classes to the same tables to create a "view" or you can use HQL to select a subset of the columns mapped by other persistent classes.</p>

<p>HTH</p>


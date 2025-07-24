# Is it possible to use Nhibernate with partition of an object over several tables?
[Link to question](https://stackoverflow.com/questions/9363386/is-it-possible-to-use-nhibernate-with-partition-of-an-object-over-several-tables)
**Creation Date:** 1329750790
**Score:** 0
**Tags:** nhibernate, mapping, database-partitioning
## Question Body
<p>We are having a system that gather large quantities of data each month and performes rather advanced calculations that increase the database even more. Since we have the requirements from the customer that we need to store data for fast access three years back and that we must be able to access older data (up to ten years), this however can be low performance and requires some work. We want to avoid performance issues where the database and its tables grows out of proportion.</p>

<p>After discussing using SQL Enterprise (VERY costly and full of traps since we haven't gotten the know-how) and since our system have so many tables that referenses each other we are leaning towards creating some kind of history tables to which we move data in a monthly fashion and rewrite the select queries that we have based on parameters to search either in the regular table or in the history or both depending on the situation.</p>

<p>Since we also are using NHibernate for mapping I was wondering if it is possbible to create a mapping file that handles this by itself (almost) using some sort of polymorfism or inheritance in which each object is stored in different tables based on parameters?</p>

<p>I know this sounds complicated and strange and that there is other methods to perform this but I this question I would rather have people answering the question asked and not give other sugestions to use instead.</p>

## Answers
### Answer ID: 9366166
<p>Short answer "no". I would not create views as you mention a lot of joining.</p>

<p>Personally I would create summary tables and map to these directly using a stateless session or a very least <code>mutable=false</code> on the class definition. Think of these summary tables as denormalised data for report only. The only drawback is if historic data changes on a regular basis then the summary tables also needs changing. If historical data never changes then this should be simple to achieve.</p>

<p>I would also most probably store these summary tables on another catalog rather than adding to the size of the current system.</p>

<p>Its not a quick win this one I am afraid.</p>

### Answer ID: 9363504
<p>As far as I know NHibernate can't do that (each class can be mapped to one table/view )but you can use SQL Queries or StoredProcedures (depends on the version of NHibernate that you are using) to populate mapped objects.
In your case you can have a combined view created by making unions of different tables Then you can use a SQL query to populated your entity.
There's also another solution that you create a summary object for your queries that uses that view ,therefore you can use both HQL and criteria to query this object.</p>


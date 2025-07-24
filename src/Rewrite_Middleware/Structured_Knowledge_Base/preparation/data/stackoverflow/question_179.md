# Low-level SQL optimisation with Entity Framework
[Link to question](https://stackoverflow.com/questions/1571194/low-level-sql-optimisation-with-entity-framework)
**Creation Date:** 1255598127
**Score:** 1
**Tags:** database, entity-framework, optimization
## Question Body
<p>In the past when working with databases I've found it necessary to do low-level tweaks to the query, for example providing hints to the optimiser that it should use a particular index or join order. We are currently considering rewriting our data layer using Entity Framework; is it the case that using EF prevents this sort of low-level optimisation?</p>

<p>In answer to <a href="https://stackoverflow.com/questions/1233245/how-to-optimize-entity-framework-queries">this question</a> it was suggested that reworking the LINQ query was the best way of ensuring that the query against the underlying database was efficient, but surely this is contrary to the stated goal of the Entity Framework that it should separate physical-layer concerns from the code, which should only deal with the conceptual layer.</p>

<p>One option is to use a view. Another option is apparently to tweak the defining query for an entity type. However, both these approaches operate per-entity-type, and optimisation tweaks often need to be applied for only some uses of a table, not every use of a table. I'm worried that I'm going to end up having to introduce pseudo-entities into the conceptual layer in order to take advantage of this, again detracting from the separation of conceptual and physical layers.</p>

## Answers
### Answer ID: 1572515
<p>Even though a compiler will optimse you code, if you write loops, in loops, in loops it will go slow.</p>

<p>If you load sub tables with "Inculde" or "load" you will get different number of hits to the database.</p>

<p>The way you write your LINQ queries will affect the SQL that is produced.</p>

<p>The way that I do it is to check the sql that is being produced by looking at the output in SQL profiler.</p>

<p>We might get where you want to be, when we have in memory databases :)</p>

### Answer ID: 1572325
<p>Well, since I wrote the answer to which you refer, perhaps I should clarify. LINQ queries which are <em>badly written as LINQ</em> should be rewritten, because bad LINQ rarely becomes good SQL. So write the best LINQ you possibly can, not because you're trying to tweak the SQL, per se, but because you need to start with something which is good on its own terms.</p>

<p>Beyond that, however, if you need to optimize a specific query, then you probably want to map a stored procedure. Aside from giving you total control, this allows you to do things which are not normally supported in any LINQ implementation.</p>

### Answer ID: 1571859
<p>I am not an Entity Framework expert, so I am certain that there are parts of it that I misunderstand, but I do know that one of the reasons that any SQL Server DBA's are "reluctant" to endorse ORM's in general is that this issue of low-level code tuning for performance has not been reasonably addressed. The general vibe that I get from some of the EF adherants is that the SQL Server Opimization Engine gets better with each release, so such low-level coding shouldn't be necessary for most applications.</p>

<p>That being said, if you need high-performance from a SQL Server and you cannot afford a machine upgrade, then I'm afraid you'll need to continue to manage your SQL code (you could perhaps use LINQ to SQL); if the application is small, and the need for performance is mitigated by the amount of data stored, you could probably use the EF and rely on the optimizer.</p>


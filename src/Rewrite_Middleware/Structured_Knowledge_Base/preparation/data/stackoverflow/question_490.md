# Using an ORM with a database that has no defined relationships?
[Link to question](https://stackoverflow.com/questions/2829593/using-an-orm-with-a-database-that-has-no-defined-relationships)
**Creation Date:** 1273778077
**Score:** 1
**Tags:** nhibernate, database-design, orm, datamapper
## Question Body
<p>Consider a database(MSSQL 2005) that consists of 100+ tables which have primary keys defined to a certain degree. There are 'relationships' between tables, however these are not enforced with foreign key constraints.</p>

<p>Consider the following simplified example of typical types of tables I am dealing with. The are clear relations between the User and City and Province tables. However, they key issues is the inconsistent data types in the tables and naming conventions. </p>

<pre><code>User:
    UserRowId [int] PK
    Name [varchar(50)]
    CityId [smallint]
    ProvinceRowId [bigint]

City:
    CityRowId [bigint] PK
    CityDescription [varchar(100)]

Province:
    ProvinceId [int] PK
    ProvinceDesc [varchar(50)]
</code></pre>

<p>I am considering a rewrite of the application (in ASP.net MVC) that uses this data source as is <em>similar</em> in design to MVC storefront. However I am going through a proof of concept phase and this is one of the stumbling blocks I have come across.</p>

<ol>
<li><p>What are my options in terms of ORM choice that can be easily used and why? </p></li>
<li><p>Should I even be considering an ORM? (The reason I ask this is that most explanations and tutorials all work with relatively cleanly designed existing databases, or newly created ones when compared to mine. I am thus having a very hard time trying to find a way forward with this problem)</p></li>
<li><p>There is a huge amount of existing SQL queries, would a datamappper(eg IBatis.net) be more suitable since we could easily modify them to work and reuse the investment already made?</p></li>
</ol>

<p>I have found <a href="https://stackoverflow.com/questions/2609625/nhibernate-legacy-database-foreign-keys-that-arent">this question</a> on SO which indicates to me that an ORM can be used - however I get the impression that this a question of mapping? </p>

<p>Note: at the moment, the object model is not clearly defined as it was non-existent. The existing system pretty much did almost everything in SQL or consisted of overly complicated, and numerous queries to complete functionality. I am pretty much a noob and have zero experience around ORMs and MVC - so this an awesome learning curve I am on.</p>

## Answers
### Answer ID: 2835330
<p>We've just faced this problem with an awful schema design (randomly has primary keys, no foreign keys at all, badly designed tables - just a mess).</p>

<p>We had the luxury of technology choice, and went MVC2 front end (irrelevant to your question), and had 2 devs split off - one try to model using NHibernate, the other using Entity Framework 4.</p>

<p>I hasten to add that we had a strong idea of what we wanted from our domain model, and modelled that first (not wanting to be constrained by the database), so our 'User' object from a schema point of view actually spanned 5 tables, we encapsulated a lot of the business logic so that the domain model wasn't aneamic, and once we were happy with our User object, we started the process of trying to plugin the ORM.</p>

<p>I can say without hesitation in both cases (NH and EF4) the compromises we had to make on our model in order to shoe-horn the implementation in was phenomenal.  I'll give you the examples from EF4 as that's the one I was most closely involved in, others may be able to relate these to other ORMs.</p>

<p><strong>private setters</strong></p>

<p>Nope - not on your life with EF4.  Your properties must be public.  There are workarounds (for example, creating wrappers around properties that were coming in from your DB)</p>

<p><strong>enums</strong></p>

<p>Again, no - there was a wrapper concept and a 'mapping' to try to get a lookup int out of the DB into the models enum types.</p>

<p><strong>outcomes</strong></p>

<p>We persevered for a while with both approaches to get to a point where we'd completed the mapping of a user, and the outcome was that we had to compromise our domain model in too many ways.</p>

<p><strong>where did we go after that?</strong></p>

<p>Linq to SQL with our own mapping layer.  And we've never looked back - absolutely fantastic - we've written the mapping layer ourselves once that takes the Dto object down at the Dal layer and maps it (as we specify it) into our Domain model.</p>

<p>Good luck with any investigation of ORMs, I'd certainly re-investigate them if I had a decent schema to base them off, but as it stood, with an awful schema, it was easier to roll our own.</p>

<p>Cheers,
Terry </p>

### Answer ID: 2829836
<p>I agree with Ben.</p>

<p>I was in this situation with a LAMP stack. An old dirty, bady coded website needed bringing up to scratch. It was literally the worst database I have seen, coupled with line after line of blind SQL execution.</p>

<p>Job? Get rid of all that SQL very quickly and replace it with an abstraction. Which ORM? I found that using an existing ORM to fit over a bad database (most databases really) retrospectively is bad news. I think this is a problem with ORMs, they move database/storage concerns closer to the application  ... not further away.</p>

<p><strong>My Solution:</strong> A reflective ORM that used only the existing database state to work out what was going on. All selects, inserts, updates and what-not used views/stored proceedures to mask the cruddy database. It is powered by a linq-esque API just rewrite the grim SQL with. Boiled around 100klocs SQL statements down to less than 2klocs.</p>

<p><strong>pros</strong>: I can gradually port the database to a better structure behind the views and proceedures. IMHO this is how <em>all databases should be organised</em>, taking full advantage of the abstraction that SPs and views provide. I never want to see a single SQL statement (or an ORM masquerading as SQL) directly against a table.</p>

<p>That's my story. An overengineered way to slot a nice abstraction above an existing and crap database, without rewriting the database first, and without crowbaring an ORM into the mix making things much more complex.</p>

<p><strong>a hack, no doubt</strong>, but it works so well I am using it in projects where I can design the database from scratch anyway ;)</p>

### Answer ID: 2829681
<p>The amount of work involved in trying to keep the existing schema and then crowbaring it into a much more structured orm pattern would probably be large and complex. If you are rewriting the whole system and retiring the old one then i would devise my data model create a new db and set of classes,maybe using linq2sql, then write a data migration script to move the data from the old schema to the new one.  That way your complex fiddly code is all in the migration and you don't have to deal with maintining and managing a complex mapping between a structured class model and a badly designed db.</p>


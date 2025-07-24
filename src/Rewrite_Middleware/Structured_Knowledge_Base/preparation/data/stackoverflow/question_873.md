# Sharding existing postgresql database with PostgresXL
[Link to question](https://stackoverflow.com/questions/47791806/sharding-existing-postgresql-database-with-postgresxl)
**Creation Date:** 1513164088
**Score:** 3
**Tags:** django, postgresql, postgres-xl
## Question Body
<p>We want to shard our PostgreSQL DB, due to high disk load. Firstly, we looked at <a href="https://github.com/JBKahn/django-sharding" rel="nofollow noreferrer">django-sharding library</a>, but:</p>

<ol>
<li>Very much rewriting in our backend</li>
<li>Migrating all tables to 64-bit primary keys is hard work on 300-400gb tables</li>
<li>Generating ids with Postgres Specific algorithm makes it impossible to move data from shard to shard. More than that, we have a large database with old ids. Updating all of them is a big problem too.</li>
<li>Generating ids with special tables makes us do a special SELECT query to main database every time we insert data. We have high write load, so it's not good.</li>
</ol>

<p>Considring all these, we decided too look on Postgres database sharding solutions. We found 2 opportunities - Citus and PostgresXL. Citus makes us change data format too much and rewrite a big bunch of backend at the same time, so we are about to try PostgresXL as more transparent solution. But reading the docs, I can't understand some things and will be greatfull for recomendations:</p>

<ol>
<li>Are there any other sharding workarounds except for Citus and PostgresXL? It would be good not to change much in our database on migrating.</li>
<li>Some questions about PostgresXL:

<ul>
<li>Do I understand correctly, that it's not Postgres extension, it's a standalone fork? So I should build all its parts from sources and than move data in some way?</li>
<li>How are Postgres and PostgresXL versions compatible? We have PostgreSQL 9.4. I don't see such a version in PostgresXL (9.2 or 9.5 no middle?). So can I use, for example, streaming replication for migration? </li>
<li>If yes/no, what is the best solution to migrate data? If I have 2Tb database with heavy write, can I migrate it somehow without stopping for a long period of time?</li>
</ul></li>
</ol>

<p>Thanks.</p>

## Answers
### Answer ID: 48158570
<p>First off to save your self a LOT of headache have you looked at options Like Amazon's Auora, Dynomo, Red Shift, etc services?  They are VERY cost effective at scale, as well as optimized and managed for you.   </p>

<p>Actually Amazon's straight Postgress databases can handle MASSIVE amounts of reads or writes.  We can go into 2,000- 6,000 IOPS on reads and another 2,000 to 6,000 IOPS in writes without issue.  I would really look into this as the option.  Azure, Oracle, and Google also have competing services.</p>

<p>Also be aware that Postgres-XL beyond all reason has no HA support.   If you lose a single node you lose everything.   The nodes can not fail over.</p>

<blockquote>
  <p>it's a standalone fork?</p>
</blockquote>

<p>Yes,   They are very different apps and developed separate from each other.</p>

<blockquote>
  <p>How are Postgres and PostgresXL versions compatible?</p>
</blockquote>

<p>They arn't compatible.  You can not just migration Postgres to Postgresl-XL.  They work VERY differently.   </p>

<blockquote>
  <p>Generating ids with Postgres Specific algorithm makes it impossible to >move data from shard to shard</p>
</blockquote>

<p>Not following this, but with sharing you are not supposed to move data from one shard to another.   The key being used generally needs to be something specific and unique to split/segregate your data on.   Like a date, or a "type" field, or some other (hopefully ordered) field(s)/column(s).  This breaks things up but has obvious pain in the a$$ limitations.</p>

<blockquote>
  <blockquote>
    <p>Are there any other sharding workarounds except for Citus and 
    PostgresXL? It would be good not to change much in our database on >>migrating.</p>
  </blockquote>
</blockquote>

<p>Tons of options, but right off the bat going from a standard RDS, to a NoSql, or MPP database is going to be a major migration, a lot of effort, and have a LOT of limitations no matter what you do.  </p>

<p>Next Postress-XL and Citus are MPP (massive parallel processing) clustering apps, not sharing specifically.  That is part of what they can do, but it is not their focus.</p>

<p><strong>Other options for MPP</strong> </p>

<p>pgPool -- (not great for heavy writes )</p>

<p>haProxy -- ( have not done it but read about it.   Lost of work to setup and maintain. )</p>

<p>MySql Cluster -- (Huge pain to use the OSS version and major $$$ for the commercial version)</p>

<p>Green Plumb</p>

<p>Teradata </p>

<p>Vertica</p>

<blockquote>
  <p>what is the best solution to migrate data? </p>
</blockquote>

<p>Very unlikely to find a simple migration for this kind of switch.  You can expect to likely need to export the data your self from the existing RDS and import it to the new DB and will likely have to write something your self to get it the way you want it.</p>


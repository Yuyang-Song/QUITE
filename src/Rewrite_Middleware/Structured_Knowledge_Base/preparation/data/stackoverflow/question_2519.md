# Java WebApp choosing JTA, database replicator/load-balancer or both
[Link to question](https://stackoverflow.com/questions/38245624/java-webapp-choosing-jta-database-replicator-load-balancer-or-both)
**Creation Date:** 1467894929
**Score:** 1
**Tags:** postgresql, jakarta-ee, load-balancing, database-replication, jta
## Question Body
<p>We have a webapp that is currently running on one instance of Apache Tomcat with one database instance, but the increase in traffic will soon (probably) force us to resort to load-balancing several webapp instances, and we've run into a problem that seems to have no easy answer.</p>

<p>Currently our JDBC DataSource is configured as Resource-local, rather than Transactional, and after some searching, everyone recommends to use Transactional, which requires the use of a JTA provider. No real justification is used for why I don't just stick with the current scenario where we have a servlet filter catch any unhandled exceptions and rollback the active transaction. Besides that the only one I've found that is <em>just</em> a JTA provider (not with 5 more JEE technologies combined) and is still maintained is Bitronix. The other alternative is to move out of Tomcat and use Glassfish, since it is a full Java EE platform, and we also use JavaMail, JPA and JAX-RS.</p>

<p>Only one transaction scenario uses Serializable isolation level.</p>

<p>As for the database, we may be looking too far ahead to think of distributed storage like Postgres-XL or pgpool, but if we make the wrong choice now it will be harder to fix later.</p>

<p>My questions are as follows:</p>

<ul>
<li>Do synchronous database replication tools and JTA complete each-other, hinder each-other or just perform the same consistency checks twice?</li>
<li>Do we need JTA if we only have one database, but multiple webapp instances?</li>
<li>Do we need JTA if we have multiple database and multiple webapp instances?</li>
<li>Should we just switch to Glassfish or something like TomEE?</li>
</ul>

<p>Supposedly there are ways we can keep using Hibernate as our JPA under both. It would be tedious to have to rewrite all our native queries to use positional parameters because EclipseLink and OpenJPA don't support them. That little extra feature makes Hibernate worth choosing above all other JPAs for me.</p>


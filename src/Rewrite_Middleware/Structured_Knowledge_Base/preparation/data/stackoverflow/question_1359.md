# select new (JPQL Constructor Expression) in jpa/hibernate causes &quot;lazy&quot; loading for each row
[Link to question](https://stackoverflow.com/questions/72529601/select-new-jpql-constructor-expression-in-jpa-hibernate-causes-lazy-loading)
**Creation Date:** 1654597509
**Score:** 4
**Tags:** java, hibernate, jpa, orm, jpql
## Question Body
<p>Recently I found no obvious behaviour when using <a href="https://docs.oracle.com/cd/E12839_01/apirefs.1111/e13946/ejb3_langref.html#ejb3_langref_constructor" rel="nofollow noreferrer">'select new/constructor expression'</a>  in jpa/hibernate. It uses kind of lazy loading for each entity in each row in result set what is not efficient.</p>
<h2>Test example</h2>
<pre><code>@Value
public class PojoTuple {
    Entity1 e1;
    Entity2 e2;
}

@Entity
@Table(name = &quot;entity1&quot;, schema = DEFAULT_DATABASE_SCHEMA)
@NoArgsConstructor(access = PROTECTED)
public class Entity1 {

    @Id
    @Column(name = &quot;id&quot;, nullable = false)
    private String id;

    @Column(name = &quot;field1&quot;, nullable = false)
    private String field1;
}

@Entity
@Table(name = &quot;entity2&quot;, schema = DEFAULT_DATABASE_SCHEMA)
@NoArgsConstructor(access = PROTECTED)
public class Entity2 {

    @Id
    @Column(name = &quot;id&quot;, nullable = false)
    private String id;

    @Column(name = &quot;fkentity1&quot;, nullable = false)
    private String entity1Id;

    @Column(name = &quot;field2&quot;, nullable = false)
    private String field2;
}

create table entity1
(
    id     varchar2(22 char) not null primary key,
    field1 varchar2(50 char) not null
);

create table entity2
(
    id        varchar2(22 char) not null primary key,
    fkentity1 varchar2(22 char) not null,
    field2    varchar2(50 char) not null

);

insert into entity1 (id, field1) values ('10', 'anyvalue1');
insert into entity1 (id, field1) values ('11', 'anyvalue2');

insert into entity2 (id, fkentity1, field2) VALUES ('20', '10', 'anyvalue3');
insert into entity2 (id, fkentity1, field2) VALUES ('21', '11', 'anyvalue4');
</code></pre>
<h2>First case</h2>
<p>we issue a query using <em>select new</em> technique:</p>
<pre><code>Query query = entityManager.createQuery(&quot;select new my.package.PojoTuple(e1, e2) &quot; +
                                        &quot;from Entity1 e1 &quot; +
                                        &quot;join Entity2 e2 on e1.id=e2.entity1Id &quot;);
query.getResultList();
</code></pre>
<p>This issues one query to fetch <strong>only ids</strong> of e1 and e2 and then more queries to fetch e1, e2 by id one by one for each row in result set:</p>
<blockquote>
<p>Query:[&quot;select entity1x0_.id as col_0_0_, entity2x1_.id as col_1_0_
from schema.entity1 entity1x0_ inner join schema.entity2 entity2x1_ on
(entity1x0_.id=entity2x1_.fkentity1)&quot;]</p>
<p>Query:[&quot;select entity1x0_.id as id1_1_0_, entity1x0_.field1 as
field2_1_0_ from schema.entity1 entity1x0_ where entity1x0_.id=?&quot;]
Params:[(10)]</p>
<p>Query:[&quot;select entity2x0_.id as id1_2_0_, entity2x0_.fkentity1 as
fkentity2_2_0_, entity2x0_.field2 as field3_2_0_ from schema.entity2
entity2x0_ where entity2x0_.id=?&quot;] Params:[(20)]</p>
<p>Query:[&quot;select entity1x0_.id as id1_1_0_, entity1x0_.field1 as
field2_1_0_ from schema.entity1 entity1x0_ where entity1x0_.id=?&quot;]
Params:[(11)]</p>
<p>Query:[&quot;select entity2x0_.id as id1_2_0_, entity2x0_.fkentity1 as
fkentity2_2_0_, entity2x0_.field2 as field3_2_0_ from schema.entity2
entity2x0_ where entity2x0_.id=?&quot;] Params:[(21)]</p>
</blockquote>
<h2>Second case</h2>
<p>Whereas rewriting sample from above to:</p>
<pre><code>Query query = entityManager.createQuery(&quot;select e1, e2 &quot; +
                                        &quot;from Entity1 e1 &quot; +
                                        &quot;join Entity2 e2 on e1.id=e2.entity1Id &quot;);

query.getResultList();
</code></pre>
<p>Issues exactly one query to database with all required fields selected:</p>
<blockquote>
<p>Query:[&quot;select entity1x0_.id as id1_1_0_, entity2x1_.id as id1_2_1_,
entity1x0_.field1 as field2_1_0_, entity2x1_.fkentity1 as
fkentity2_2_1_, entity2x1_.field2 as field3_2_1_ from schema.entity1
entity1x0_ inner join schema.entity2 entity2x1_ on
(entity1x0_.id=entity2x1_.fkentity1)&quot;]
Params:[()]</p>
</blockquote>
<h2>Question</h2>
<p>From my perspective there is no big difference how these two queries should be performed. First case issues many queries that I do not expect what is highly inefficient. Second case works as expected issuing exactly one query to database. Is this a bug, suboptimal solution or some hidden feature that I can not see?</p>
<p>Environment
hibernate-core: 5.6.9.Final</p>

## Answers
### Answer ID: 72571717
<p>So I finally found partial explanation from the most authoritative source of knowledge about hibernate I know - Vlad Mihalcea: <a href="https://vladmihalcea.com/why-you-should-use-the-hibernate-resulttransformer-to-customize-result-set-mappings/" rel="nofollow noreferrer">Paragraph: Returning an entity in a DTO projection</a></p>
<blockquote>
<p>However, there might be use cases when you want to select an entity inside your DTO projection.
(...)</p>
<p>When you execute a JPQL query like this one:</p>
<pre><code>List&lt;PersonAndCountryDTO&gt; personAndAddressDTOs = entityManager.createQuery(
&quot;select new &quot; +
&quot;   com.vladmihalcea.book.hpjp.hibernate.query.dto.PersonAndCountryDTO(&quot; +
&quot;       p, &quot; +
&quot;       c.name&quot; +
&quot;   ) &quot; +
&quot;from Person p &quot; +
&quot;join Country c on p.locale = c.locale &quot; +
&quot;order by p.id&quot;, PersonAndCountryDTO.class) .getResultList();
</code></pre>
<p>Hibernate generates the following SQL queries:</p>
<pre><code>SELECT p.id AS col_0_0_,
   c.name AS col_1_0_ FROM   Person p INNER JOIN
   Country c ON
   ( p.locale = c.locale ) ORDER BY
   p.id   

SELECT p.id AS id1_1_0_,
   p.locale AS locale2_1_0_,
   p.name AS name3_1_0_ FROM   Person p WHERE  p.id = 3   

SELECT p.id AS id1_1_0_,
   p.locale AS locale2_1_0_,
   p.name AS name3_1_0_ FROM   Person p WHERE  p.id = 4
</code></pre>
<p>The Hibernate 5.2 implementation of the DTO projection cannot
materialize the DTO projection from the ResultSet without executing a
secondary query. However, this is very bad to performance since it can
lead to N+1 query issues.</p>
<p>This HQL limitation has been discussed, and Hibernate 6.0 new SQM parser might address this issue, so stay tuned!</p>
</blockquote>
<p>So to summarize:</p>
<ol>
<li>Behaviour I asked about is known to hibernate developers and there is a hope it will be fixed.</li>
<li>As for now one has to know that extracting complete, managed entities with constructor expression is completely fine as a design, but with hibernate 5.x can lead to non optimal solution due to many queries issued by hibernate</li>
</ol>

### Answer ID: 72530210
<p>You should not return entities in objects created with the constructor expression. That's not the intention of this feature and that's also the reason why it loads the data with many queries.</p>
<p><a href="https://docs.jboss.org/hibernate/orm/current/userguide/html_single/Hibernate_User_Guide.html#hql-select-new" rel="nofollow noreferrer">https://docs.jboss.org/hibernate/orm/current/userguide/html_single/Hibernate_User_Guide.html#hql-select-new</a></p>


# JPQL join translation policy
[Link to question](https://stackoverflow.com/questions/40567261/jpql-join-translation-policy)
**Creation Date:** 1478982076
**Score:** 0
**Tags:** mysql, jpa, jakarta-ee, jpql
## Question Body
<p>I am having trouble searching in my application database due to the translated query resulting from my JPQL query.</p>

<p>Consider the following Structure:</p>

<pre><code>@Entity
@Table(name="pc")
public class PC {

    @Id
    @GeneratedValue
    private Long id;

    @Column
    private String name;

    @ManyToOne
    @JoinColumn(name="DEFAULTOS")
    private Software defaultOS;
    ...}

@Entity
@Table(name="software")
public class Software {

    @Id
    @GeneratedValue
    private Long id;

    @Column
    private String name;
    ...}
</code></pre>

<p>Here is the search query I'm doing:</p>

<pre><code>public List&lt;PC&gt; getPcsInstalled(Software soft){
    TypedQuery&lt;PC&gt; lQuery = em.createQuery("SELECT lPC FROM PC lPC"
            + " WHERE lPC.defaultOS IS NULL"
            + " OR lPC.defaultOS.name NOT LIKE :param", PC.class);
    lQuery.setParameter("param", soft.getName());
    return lQuery.getResultList();  
}
</code></pre>

<p>Which translates to:</p>

<pre><code>SELECT t1.ID, t1.NAME, t1.DEFAULTOS FROM software t0, pc t1
WHERE (((t1.DEFAULTOS IS NULL) OR NOT (t0.NAME LIKE "Linux"))
AND (t0.ID = t1.DEFAULTOS))
</code></pre>

<p>The tables are "joined" with the latest condition <code>(t0.ID = t1.DEFAULTOS)</code>. Which automatically filters any PC having DEFAULTOS = NULL (which is not what I want obviously).</p>

<p>The query I expected was:</p>

<pre><code> SELECT t1.ID, t1.NAME, t1.DEFAULTOS FROM pc t1
 LEFT JOIN software t0 ON t1.DEFAULTOS = t0.ID
 WHERE (((t1.DEFAULTOS IS NULL) OR NOT (t0.NAME LIKE "Linux")))
</code></pre>

<p>Of course I can rewrite the JPQL query to specify the LEFT JOIN explicitely, but I was wondering : <strong>Is there a way to have the LEFT JOIN as the default policy to join tables?</strong></p>

<p>In fact this is just a simple example, in my project I build much more complex queries and adding the needed LEFT JOIN would be very complex in the actual code.</p>

<p>For information, I'm using Glassfish 4.0 with EclipseLink and a MySQL database.</p>


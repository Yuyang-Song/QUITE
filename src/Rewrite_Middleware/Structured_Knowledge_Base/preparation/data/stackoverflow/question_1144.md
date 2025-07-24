# Hibernate @Entity conflict with Spring @Autowired for non-column object
[Link to question](https://stackoverflow.com/questions/60852934/hibernate-entity-conflict-with-spring-autowired-for-non-column-object)
**Creation Date:** 1585153256
**Score:** 1
**Tags:** java, spring, hibernate, autowired
## Question Body
<p>I have a table which contains item descriptions. Items have a price history which can be very extensive. It's that last bit that leads me to avoid using a normal one-to-many Hibernate mapping with lazy loading. Think a price history like ticks on a stock exchange, <em>lots</em> of history. </p>

<p>So I have a cache which works well, it's all wired with Spring, the DAO is injected, the cache manages what needs to be queried vs what it already knows.</p>

<p>So, the "natural" thing is to be able to ask an item about it's price history. Here's some code, which is a slimmed down version of the real thing:</p>

<pre><code>@Entity @Table(name="item")
public class Item {
    @Id
    @Column(name="id")
    private long id;
    @Column(name="name")
    private String name;

    @Autowired
    private PriceCache priceCache;

    /* ...setters, getters for id, name ... */

    public NavigableMap&lt;LocalDateTime,SecurityValue&gt; getPrices(LocalDateTime begTime, LocalDateTime endTime) {
        return priceCache.get(id, begTime, endTime);
    }
}
</code></pre>

<p>My original version used all static methods with PriceCache; I want to switch to using an injected bean in part because it will mean I can rewrite the cache as an implementation of an interface which makes it easier to set up unit tests for some bits that aren't in the example; I can create a test cache object that supplies my price history in whatever way I need to the test without ever going to the database.</p>

<p>The problem is that when Spring and Hibernate scan the packages, they seem to conflict over what to do with that @Autowired field; I get the following with some formatting for readability); dbEMF is my EntityManagerFactory:</p>

<pre><code>Exception in thread "main" org.springframework.beans.factory.BeanCreationException:
   Error creating bean with name 'dbEMF' defined in class path resource [applicationContext.xml]:
     Invocation of init method failed;
   nested exception is javax.persistence.PersistenceException:
     [PersistenceUnit: default] Unable to build Hibernate SessionFactory;
   nested exception is org.hibernate.MappingException:
     Could not determine type for: com.example.cache.PriceCache, at table: item, for columns: [org.hibernate.mapping.Column(priceCache)]
</code></pre>

<p>Again, the basic code and cache work fine provided I use only static methods with the PriceCache, where I create it as a singleton "manually". Converting it to let Spring handle the creating and injection elsewhere works just fine, too. It's only when I have this mix of Hibernate and Spring that I run into a problem.</p>

<p>I haven't tried going back to using an external XML file for the hibernate config which might solve the issue, or not.</p>

<p>Is there a way to tell Hibernate this is <em>not</em> a column? Or is there a different pattern I should be following to do this sort of thing, maybe some sort of proxy for the Item objects?</p>

## Answers
### Answer ID: 60870339
<p>Regarding the discussion in the answer below.
Hibernate collections and entities are all proxied objects.
Maybe what you can try is to implement a custom HibernateProxy that will manage your collection.
As per the docs it seems to be possible (CustomProxies) but I have never done it check here: <a href="https://docs.jboss.org/hibernate/orm/5.4/userguide/html_single/Hibernate_User_Guide.html#entity-proxy" rel="nofollow noreferrer">https://docs.jboss.org/hibernate/orm/5.4/userguide/html_single/Hibernate_User_Guide.html#entity-proxy</a> </p>

### Answer ID: 60853220
<p>you can use <code>@Transient</code> annotation, to indicate it should not be persisted into DB.   </p>

<p>Generally speaking, I think if this is an entity, it should not have any autowired cache which is not part of it, but that's a different story</p>


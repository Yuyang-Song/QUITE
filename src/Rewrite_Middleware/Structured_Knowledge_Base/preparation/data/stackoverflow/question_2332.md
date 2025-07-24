# How does hibernate distinguish entity types in native query in case of inheritance. What is the real meaning of clazz_ column?
[Link to question](https://stackoverflow.com/questions/29764885/how-does-hibernate-distinguish-entity-types-in-native-query-in-case-of-inheritan)
**Creation Date:** 1429598969
**Score:** 3
**Tags:** java, oracle-database, hibernate, jpa, inheritance
## Question Body
<p>I have a hierarchy of entities:</p>

<pre><code>@Entity
@Inheritance(strategy = InheritanceType.JOINED)
class A {
  @Id
  private Long id;
}

@Entity
@PrimaryKeyJoinColumn(name = "id", referencedColumnName = "id")
class B extends A {
}
</code></pre>

<p>And a query which retrieves A entities when record in table B does not exist and B entities in other case. I created JPQL query and it worked perfectly, but query had too high cost at the database side. So I decided to create native query and map it to entities. I was wondering how to let Hibernate know which entity should be returned and I found some solution:</p>

<p><a href="https://stackoverflow.com/questions/2140992/jpa-native-query-for-entity-with-inheritance">JPA Native Query for Entity with Inheritance</a></p>

<pre><code>entityManager.createNativeQuery("select a.*, b*, 1 as clazz_, from A a LEFT OUTER JOIN B b on id = a.id where procedure(f)",A.class).getResultList()
</code></pre>

<p>It looks like there is a special artificial column to distinguish between types. My JPQL query when translated to SQL also had this column. In above example this column has always value of <code>1</code>. In my JPQL query it rather looked like:</p>

<pre><code>case when cim.id is not null then 1 when ci.id is not null then 0 end as clazz_
</code></pre>

<p>I can just rewrite this into my native query, but how can I be sure that mapping of values <code>0</code> and <code>1</code> to given types won't change next time? What if I add another class extending A?</p>

## Answers
### Answer ID: 29789323
<p>The <a href="https://github.com/hibernate/hibernate-orm/blob/master/hibernate-core/src/main/java/org/hibernate/persister/entity/JoinedSubclassEntityPersister.java" rel="nofollow">JoinedSubclassEntityPersister</a> defines an <code>IMPLICIT_DISCRIMINATOR_ALIAS</code> property:</p>

<pre><code>private static final String IMPLICIT_DISCRIMINATOR_ALIAS = "clazz_";
</code></pre>

<p>Which is used when you don't specify an explicit discriminator value:</p>

<pre><code>explicitDiscriminatorColumnName = null;
discriminatorAlias = IMPLICIT_DISCRIMINATOR_ALIAS;
discriminatorType = StandardBasicTypes.INTEGER;
try {
    discriminatorValue = persistentClass.getSubclassId();
    discriminatorSQLString = discriminatorValue.toString();
}
catch ( Exception e ) {
    throw new MappingException( "Could not format discriminator value to SQL string", e );
}
</code></pre>

<p>The <code>0</code> and <code>1</code> values come from <code>persistentClass.getSubclassId();</code> which is assigned by Hibernate at runtime:</p>

<pre><code>public Subclass(PersistentClass superclass) {
    this.superclass = superclass;
    this.subclassId = superclass.nextSubclassId();
}
</code></pre>

<p>the RootClass default id being <code>0</code>:</p>

<pre><code>@Override
public int getSubclassId() {
    return 0;
}
</code></pre>

<p>Because the identifiers are assigned at runtime, it's unclear what will happen if a new subclass is added and it's being loaded prior to some already existing ones, so you are better off setting this value explicitly and bypass the implicit subclass ids:</p>

<pre><code>@Entity
@Inheritance(strategy = InheritanceType.JOINED)
@DiscriminatorColumn(name = "discriminator", discriminatorType = DiscriminatorType.INTEGER)
class A {
  @Id
  private Long id;
}

@Entity
@PrimaryKeyJoinColumn(name = "id", referencedColumnName = "id")
@DiscriminatorValue(value = 1)
class B extends A {
}
</code></pre>

<p>or even better, specify a <code>STRING</code> discriminator:</p>

<pre><code>@Entity
@Inheritance(strategy = InheritanceType.JOINED)
@DiscriminatorColumn(name = "discriminator", discriminatorType = DiscriminatorType.STRING)
@DiscriminatorValue(value = "A")
class A {
  @Id
  private Long id;
}

@Entity
@PrimaryKeyJoinColumn(name = "id", referencedColumnName = "id")
@DiscriminatorValue(value = "B")
class B extends A {
}
</code></pre>


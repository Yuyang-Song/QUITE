# TypeMismatchException on fetching the table data by Hibernate Session.get() method
[Link to question](https://stackoverflow.com/questions/73265247/typemismatchexception-on-fetching-the-table-data-by-hibernate-session-get-meth)
**Creation Date:** 1659852243
**Score:** 0
**Tags:** java, hibernate, jpa, spring-data-jpa, jpa-2.0
## Question Body
<p>In a application, having a database table <strong>CUSTOMERS</strong> defined as:</p>
<pre><code>create table CUSTOMERS (
  ID varchar(10),
  CODE varchar(10),
  CID varchar(10),
  SID varchar(10),
  FNAME varchar(50),
  LNAME varchar(50),
  constraint PK_CUSTOMERS primary key (ID, CODE, CID, SID)
);
</code></pre>
<p>and the Entity classes are created to populate the data as</p>
<pre><code>@Embeddable
public class CustKey implements Serializable , Cloneable{

    @Transient
    private static final long serialVersionUID = 1L;

    @Column(name = &quot;ID&quot;, nullable = false)
    private String id;
    
    @Column(name = &quot;CODE&quot;, nullable = false)
    private String code;
    
    @Column(name = &quot;CID&quot;, nullable = false)
    private String cid;

    @Column(name = &quot;SID&quot;, nullable = false)
    private String sid;
    
    public boolean equals(Object o){
     return id.equals(o.getId()) &amp;&amp; ...;
   }

    public int hashcode(){
     return id.hashcode() &amp; ...;
   }
}


@Entity
@Table(name = &quot;CUSTOMERS&quot;)
public class CustProfileWrapper implements Serializable,Cloneable  {

    @Transient
    private static final long serialVersionUID = 1L;
    
    @EmbeddedId
    private CustKey custKey;
    
    @Column(name = &quot;FNAME&quot;)
    private String fname;
    
    @Column(name = &quot;LNAME&quot;)
    private String lname;
}
</code></pre>
<p>The records are populated without an issue.</p>
<p>But the Entity classes are move to other project (<em>but keeping the same package name as before</em>) due to some rewrite of the code/project. but on fetching the data by Hibernate Session as</p>
<pre><code>Object object = session.get(CustProfileWrapper.class, custProfileWrapper.getCustKey(), LockMode.NONE);
</code></pre>
<p>getting the error</p>
<pre><code>org.hibernate.TypeMismatchException: Provided id of the wrong type for class CustProfileWrapper. Expected: class com.db.CustProfileWrapper, got class com.db.CustProfileWrapper 
</code></pre>
<p>However, able to get the record when using the parametrized query as</p>
<pre><code>SQLQuery query = session.createSQLQuery(&quot;SELECT * FROM CUSTOMERS WHERE ID = ? &quot;
        + &quot; AND CODE = ? AND CID = ? AND SID = ? &quot;);
query.addEntity(CustProfileWrapper.class);
query.setParameter(0, &quot;101&quot;);
...
object = query.list();
        
</code></pre>
<blockquote>
<p>But it's a low level code when using the query, and we should use the
better way like get() method.</p>
</blockquote>
<p>Any help/hint will be appreciated!!</p>
<hr />
<p>Full stack trace of the error:
<a href="https://i.sstatic.net/chkDn.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/chkDn.png" alt="stack trace1" /></a>
<a href="https://i.sstatic.net/YR4U8.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/YR4U8.png" alt="stack trace2" /></a>
<a href="https://i.sstatic.net/lOnOi.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/lOnOi.png" alt="stack trace3" /></a>
<a href="https://i.sstatic.net/VxfN4.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/VxfN4.png" alt="stack trace4" /></a></p>

## Answers
### Answer ID: 73291872
<p>After so much investigation, found the <em>culprit</em> <strong>spring-boot-devtools</strong> dependency, as explained here:</p>
<blockquote>
<p>I was getting this problem after adding a dependency to
spring-boot-devtools in my Springboot project. I removed the
dependency and the problem went away. My best guess at this point is
that spring-boot-devtools brings in a new classloader and that causes
the issue of class casting problems between different classloaders in
certain cases where the new classloader is not being used by some
threads.</p>
</blockquote>
<p>Reference: <a href="https://stackoverflow.com/questions/33955542/a-dozer-map-exception-related-to-spring-boot-devtools">A dozer map exception related to Spring boot devtools</a></p>
<p>Refs: <a href="https://stackoverflow.com/questions/826319/classcastexception-when-casting-to-the-same-class">ClassCastException when casting to the same class</a></p>


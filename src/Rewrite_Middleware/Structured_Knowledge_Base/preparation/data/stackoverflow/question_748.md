# Why I can&#39;t map a Point field of my entity class on a Point field on the database? column &quot;location&quot; is of type point but expression is of type bytea
[Link to question](https://stackoverflow.com/questions/40327188/why-i-cant-map-a-point-field-of-my-entity-class-on-a-point-field-on-the-databas)
**Creation Date:** 1477815497
**Score:** 6
**Tags:** spring, hibernate, spring-boot, spring-data-jpa, hibernate-spatial
## Question Body
<p>I am working on my first <strong>Spring Boot</strong> + <strong>Spring Data JPA</strong> + <strong>Hibernate 5</strong> working on a <strong>PostgreSQL</strong> database.</p>
<p>I have the following problem trying to map a field having <strong>point</strong> as data type (so I am using <strong>Hibernate Spatial</strong> that is natively included into Hibernate 5.</p>
<p>So I have the following situation:</p>
<p>I have the following simple database table named cities:</p>
<pre><code>Field              Type   
----------------------------------------------------------------    
id                 bigint                   (it is the PK)
name               character varying
location           point                    (it contains the coordinates)
</code></pre>
<p>So for example this table contains this record:</p>
<pre><code>id         name             location
--------------------------------------
1          San Francisco    (-194,53)
</code></pre>
<p>Then I have this <strong>Cities</strong> entity class that map the previous cities database table:</p>
<pre><code>import com.vividsolutions.jts.geom.Point;
import org.hibernate.annotations.Type;
import javax.persistence.*;
import java.io.Serializable;

@Entity
@Table(name = &quot;cities&quot;)
public class Cities implements Serializable {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = &quot;id&quot;)
    private Long id;

    private String name;

    @Column(name = &quot;location&quot;, columnDefinition=&quot;Point&quot;)
    private Point location;

    public Cities() {
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Point getLocation() {
        return location;
    }

    public void setLocation(Point location) {
        this.location = location;
    }
}
</code></pre>
<p>I am using this implementation of the <strong>Point</strong> class: <strong>com.vividsolutions.jts.geom.Point</strong> because I found it on some tutorial but I am not sure if it is correct because I also can chose these other implementations:</p>
<pre><code>org.geolatte.geom.Point
org.springframework.data.geo.Point
</code></pre>
<p>Then I have this <strong>Spring Data JPA</strong> interface that represent my DAO class:</p>
<pre><code>@Repository
public interface CitiesDAO extends JpaRepository&lt;Cities, Long&gt; {

    Cities findById(@Param(&quot;id&quot;) Long id);
}
</code></pre>
<p>As you can see it extends <strong>JpaRepository</strong> and the method signature &quot;implements&quot; my queries (using JPA).</p>
<p>So, into my JUnit test class I implemented this test method in which I am trying to insert a new record into the <strong>cities</strong> table on the database:</p>
<pre><code>@Test
public void testCitiesDAO() {
    System.out.println(&quot;testCitiesDAO() START&quot;);

    //Cities city = citiesDAO.findById(1L);


    GeometryFactory geometryFactory = new GeometryFactory();

    Coordinate coordinate = new Coordinate();
    coordinate.x = 2;
    coordinate.y = 5;

    Point myPoint = geometryFactory.createPoint(coordinate);

    Cities rome = new Cities();

    rome.setId(new Long(2));
    rome.setName(&quot;Rome&quot;);
    rome.setLocation(myPoint);

    citiesDAO.save(rome);

    System.out.println(&quot;testCitiesDAO() END&quot;);

}
</code></pre>
<p>So I am creating the object to persist (Cities rome) on which I set a brand new <strong>Point</strong> object and I am trying to persist it by this line:</p>
<pre><code>citiesDAO.save(rome);
</code></pre>
<p>The problem is that when try to perform the <strong>save(rome)</strong> method this exception is thrown:</p>
<pre><code>Hibernate: select cities0_.id as id1_0_0_, cities0_.location as location2_0_0_, cities0_.name as name3_0_0_ from cities cities0_ where cities0_.id=?
Hibernate: insert into cities (location, name) values (?, ?)
2016-10-29 20:08:09.509 ERROR 7956 --- [           main] o.h.engine.jdbc.spi.SqlExceptionHelper   : ERROR: column &quot;location&quot; is of type point but expression is of type bytea
  Hint: You will need to rewrite or cast the expression.
  Position: 45

org.springframework.dao.InvalidDataAccessResourceUsageException: could not execute statement; SQL [n/a]; nested exception is org.hibernate.exception.SQLGrammarException: could not execute statement

    at org.springframework.orm.jpa.vendor.HibernateJpaDialect.convertHibernateAccessException(HibernateJpaDialect.java:261)
    at org.springframework.orm.jpa.vendor.HibernateJpaDialect.translateExceptionIfPossible(HibernateJpaDialect.java:244)
    at org.springframework.orm.jpa.AbstractEntityManagerFactoryBean.translateExceptionIfPossible(AbstractEntityManagerFactoryBean.java:491)
    at org.springframework.dao.support.ChainedPersistenceExceptionTranslator.translateExceptionIfPossible(ChainedPersistenceExceptionTranslator.java:59)
    at org.springframework.dao.support.DataAccessUtils.translateIfNecessary(DataAccessUtils.java:213)
    at org.springframework.dao.support.PersistenceExceptionTranslationInterceptor.invoke(PersistenceExceptionTranslationInterceptor.java:147)
    at org.springframework.aop.framework.ReflectiveMethodInvocation.proceed(ReflectiveMethodInvocation.java:179)
    at org.springframework.data.jpa.repository.support.CrudMethodMetadataPostProcessor$CrudMethodMetadataPopulatingMethodInterceptor.invoke(CrudMethodMetadataPostProcessor.java:133)
    at org.springframework.aop.framework.ReflectiveMethodInvocation.proceed(ReflectiveMethodInvocation.java:179)
    at org.springframework.aop.interceptor.ExposeInvocationInterceptor.invoke(ExposeInvocationInterceptor.java:92)
    at org.springframework.aop.framework.ReflectiveMethodInvocation.proceed(ReflectiveMethodInvocation.java:179)
    at org.springframework.aop.framework.JdkDynamicAopProxy.invoke(JdkDynamicAopProxy.java:213)
    at com.sun.proxy.$Proxy105.save(Unknown Source)
    at com.betriuvis.controller.test.PlaceSearcherControllerTest.testCitiesDAO(PlaceSearcherControllerTest.java:111)
    at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
    at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
    at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
    at java.lang.reflect.Method.invoke(Method.java:497)
    at org.junit.runners.model.FrameworkMethod$1.runReflectiveCall(FrameworkMethod.java:50)
    at org.junit.internal.runners.model.ReflectiveCallable.run(ReflectiveCallable.java:12)
    at org.junit.runners.model.FrameworkMethod.invokeExplosively(FrameworkMethod.java:47)
    at org.junit.internal.runners.statements.InvokeMethod.evaluate(InvokeMethod.java:17)
    at org.springframework.test.context.junit4.statements.RunBeforeTestMethodCallbacks.evaluate(RunBeforeTestMethodCallbacks.java:75)
    at org.springframework.test.context.junit4.statements.RunAfterTestMethodCallbacks.evaluate(RunAfterTestMethodCallbacks.java:86)
    at org.springframework.test.context.junit4.statements.SpringRepeat.evaluate(SpringRepeat.java:84)
    at org.junit.runners.ParentRunner.runLeaf(ParentRunner.java:325)
    at org.springframework.test.context.junit4.SpringJUnit4ClassRunner.runChild(SpringJUnit4ClassRunner.java:252)
    at org.springframework.test.context.junit4.SpringJUnit4ClassRunner.runChild(SpringJUnit4ClassRunner.java:94)
    at org.junit.runners.ParentRunner$3.run(ParentRunner.java:290)
    at org.junit.runners.ParentRunner$1.schedule(ParentRunner.java:71)
    at org.junit.runners.ParentRunner.runChildren(ParentRunner.java:288)
    at org.junit.runners.ParentRunner.access$000(ParentRunner.java:58)
    at org.junit.runners.ParentRunner$2.evaluate(ParentRunner.java:268)
    at org.springframework.test.context.junit4.statements.RunBeforeTestClassCallbacks.evaluate(RunBeforeTestClassCallbacks.java:61)
    at org.springframework.test.context.junit4.statements.RunAfterTestClassCallbacks.evaluate(RunAfterTestClassCallbacks.java:70)
    at org.junit.runners.ParentRunner.run(ParentRunner.java:363)
    at org.springframework.test.context.junit4.SpringJUnit4ClassRunner.run(SpringJUnit4ClassRunner.java:191)
    at org.junit.runner.JUnitCore.run(JUnitCore.java:137)
    at com.intellij.junit4.JUnit4IdeaTestRunner.startRunnerWithArgs(JUnit4IdeaTestRunner.java:117)
    at com.intellij.junit4.JUnit4IdeaTestRunner.startRunnerWithArgs(JUnit4IdeaTestRunner.java:42)
    at com.intellij.rt.execution.junit.JUnitStarter.prepareStreamsAndStart(JUnitStarter.java:262)
    at com.intellij.rt.execution.junit.JUnitStarter.main(JUnitStarter.java:84)
    at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
    at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
    at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
    at java.lang.reflect.Method.invoke(Method.java:497)
    at com.intellij.rt.execution.application.AppMain.main(AppMain.java:147)
Caused by: org.hibernate.exception.SQLGrammarException: could not execute statement
    at org.hibernate.exception.internal.SQLStateConversionDelegate.convert(SQLStateConversionDelegate.java:106)
    at org.hibernate.exception.internal.StandardSQLExceptionConverter.convert(StandardSQLExceptionConverter.java:42)
    at org.hibernate.engine.jdbc.spi.SqlExceptionHelper.convert(SqlExceptionHelper.java:109)
    at org.hibernate.engine.jdbc.spi.SqlExceptionHelper.convert(SqlExceptionHelper.java:95)
    at org.hibernate.engine.jdbc.internal.ResultSetReturnImpl.executeUpdate(ResultSetReturnImpl.java:207)
    at org.hibernate.dialect.identity.GetGeneratedKeysDelegate.executeAndExtract(GetGeneratedKeysDelegate.java:57)
    at org.hibernate.id.insert.AbstractReturningDelegate.performInsert(AbstractReturningDelegate.java:42)
    at org.hibernate.persister.entity.AbstractEntityPersister.insert(AbstractEntityPersister.java:2803)
    at org.hibernate.persister.entity.AbstractEntityPersister.insert(AbstractEntityPersister.java:3374)
    at org.hibernate.action.internal.EntityIdentityInsertAction.execute(EntityIdentityInsertAction.java:81)
    at org.hibernate.engine.spi.ActionQueue.execute(ActionQueue.java:619)
    at org.hibernate.engine.spi.ActionQueue.addResolvedEntityInsertAction(ActionQueue.java:273)
    at org.hibernate.engine.spi.ActionQueue.addInsertAction(ActionQueue.java:254)
    at org.hibernate.engine.spi.ActionQueue.addAction(ActionQueue.java:299)
    at org.hibernate.event.internal.AbstractSaveEventListener.addInsertAction(AbstractSaveEventListener.java:317)
    at org.hibernate.event.internal.AbstractSaveEventListener.performSaveOrReplicate(AbstractSaveEventListener.java:272)
    at org.hibernate.event.internal.AbstractSaveEventListener.performSave(AbstractSaveEventListener.java:178)
    at org.hibernate.event.internal.AbstractSaveEventListener.saveWithGeneratedId(AbstractSaveEventListener.java:109)
    at org.hibernate.jpa.event.internal.core.JpaMergeEventListener.saveWithGeneratedId(JpaMergeEventListener.java:56)
    at org.hibernate.event.internal.DefaultMergeEventListener.saveTransientEntity(DefaultMergeEventListener.java:255)
    at org.hibernate.event.internal.DefaultMergeEventListener.entityIsTransient(DefaultMergeEventListener.java:235)
    at org.hibernate.event.internal.DefaultMergeEventListener.entityIsDetached(DefaultMergeEventListener.java:301)
    at org.hibernate.event.internal.DefaultMergeEventListener.onMerge(DefaultMergeEventListener.java:170)
    at org.hibernate.event.internal.DefaultMergeEventListener.onMerge(DefaultMergeEventListener.java:69)
    at org.hibernate.internal.SessionImpl.fireMerge(SessionImpl.java:840)
    at org.hibernate.internal.SessionImpl.merge(SessionImpl.java:822)
    at org.hibernate.internal.SessionImpl.merge(SessionImpl.java:827)
    at org.hibernate.jpa.spi.AbstractEntityManagerImpl.merge(AbstractEntityManagerImpl.java:1161)
    at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
    at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
    at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
    at java.lang.reflect.Method.invoke(Method.java:497)
    at org.springframework.orm.jpa.SharedEntityManagerCreator$SharedEntityManagerInvocationHandler.invoke(SharedEntityManagerCreator.java:298)
    at com.sun.proxy.$Proxy101.merge(Unknown Source)
    at org.springframework.data.jpa.repository.support.SimpleJpaRepository.save(SimpleJpaRepository.java:509)
    at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
    at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
    at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
    at java.lang.reflect.Method.invoke(Method.java:497)
    at org.springframework.data.repository.core.support.RepositoryFactorySupport$QueryExecutorMethodInterceptor.executeMethodOn(RepositoryFactorySupport.java:503)
    at org.springframework.data.repository.core.support.RepositoryFactorySupport$QueryExecutorMethodInterceptor.doInvoke(RepositoryFactorySupport.java:488)
    at org.springframework.data.repository.core.support.RepositoryFactorySupport$QueryExecutorMethodInterceptor.invoke(RepositoryFactorySupport.java:460)
    at org.springframework.aop.framework.ReflectiveMethodInvocation.proceed(ReflectiveMethodInvocation.java:179)
    at org.springframework.data.projection.DefaultMethodInvokingMethodInterceptor.invoke(DefaultMethodInvokingMethodInterceptor.java:61)
    at org.springframework.aop.framework.ReflectiveMethodInvocation.proceed(ReflectiveMethodInvocation.java:179)
    at org.springframework.transaction.interceptor.TransactionInterceptor$1.proceedWithInvocation(TransactionInterceptor.java:99)
    at org.springframework.transaction.interceptor.TransactionAspectSupport.invokeWithinTransaction(TransactionAspectSupport.java:281)
    at org.springframework.transaction.interceptor.TransactionInterceptor.invoke(TransactionInterceptor.java:96)
    at org.springframework.aop.framework.ReflectiveMethodInvocation.proceed(ReflectiveMethodInvocation.java:179)
    at org.springframework.dao.support.PersistenceExceptionTranslationInterceptor.invoke(PersistenceExceptionTranslationInterceptor.java:136)
    ... 41 more
Caused by: org.postgresql.util.PSQLException: ERROR: column &quot;location&quot; is of type point but expression is of type bytea
  Hint: You will need to rewrite or cast the expression.
  Position: 45
    at org.postgresql.core.v3.QueryExecutorImpl.receiveErrorResponse(QueryExecutorImpl.java:2062)
    at org.postgresql.core.v3.QueryExecutorImpl.processResults(QueryExecutorImpl.java:1795)
    at org.postgresql.core.v3.QueryExecutorImpl.execute(QueryExecutorImpl.java:257)
    at org.postgresql.jdbc2.AbstractJdbc2Statement.execute(AbstractJdbc2Statement.java:479)
    at org.postgresql.jdbc2.AbstractJdbc2Statement.executeWithFlags(AbstractJdbc2Statement.java:367)
    at org.postgresql.jdbc2.AbstractJdbc2Statement.executeUpdate(AbstractJdbc2Statement.java:321)
    at org.hibernate.engine.jdbc.internal.ResultSetReturnImpl.executeUpdate(ResultSetReturnImpl.java:204)
    ... 86 more
</code></pre>
<p>So basically the error message is:</p>
<blockquote>
<p>Caused by: org.postgresql.util.PSQLException: ERROR: column &quot;location&quot; is of type point but expression is of type bytea</p>
</blockquote>
<p>So it seems that is trying to put something wrong into the <strong>location</strong> field of the table having <strong>point</strong> as data type. Why it can't convert the <strong>com.vividsolutions.jts.geom.Point</strong> object used into the entity class?</p>
<p>This is my <strong>application.propertis</strong> file, the only configuration file in my application:</p>
<pre><code>#No auth  protected
endpoints.shutdown.sensitive=true
#Enable shutdown endpoint
endpoints.shutdown.enabled=true
logging.file=BeTriviusController.log
logging.level.org.springframework.web=DEBUG
logging.level.org.hibernate=ERROR

# Thymeleaf
spring.thymeleaf.cache:false


# DATABASE CONFIG ----------------------------------------------------------------------------------------------------
spring.datasource.url = jdbc:postgresql://localhost:5432/test1
spring.datasource.username = postgres
spring.datasource.password = Bl4tte_Te4m
spring.datasource.driver-class-name = org.postgresql.Driver

spring.jpa.properties.hibernate.current_session_context_class=org.springframework.orm.hibernate5.SpringSessionContext

spring.datasource.testWhileIdle = true
spring.datasource.validationQuery = SELECT 1

# Show or not log for each sql query
spring.jpa.show-sql = true

# Hibernate ddl auto (create, create-drop, update, validate)
spring.jpa.hibernate.ddl-auto = validate

#spring.jpa.hibernate.naming-strategy = org.hibernate.cfg.ImprovedNamingStrategy

spring.jpa.properties.hibernate.dialect=org.hibernate.spatial.dialect.postgis.PostgisDialect
</code></pre>
<p>As you can see I have set the <strong>spring.jpa.hibernate.naming-strategy</strong> to the <strong>PostgisDialect</strong> dialect to use Hibernate spatial.</p>
<p>What is wrong? What am I missing? How can I fix this issue?</p>

## Answers
### Answer ID: 61863823
<p>As of Monday, 18th May 2020</p>

<p>Dependency is as below:</p>

<pre><code>&lt;dependency&gt;
    &lt;groupId&gt;org.hibernate&lt;/groupId&gt;
    &lt;artifactId&gt;hibernate-spatial&lt;/artifactId&gt;
    &lt;version&gt;5.4.15.Final&lt;/version&gt;
&lt;/dependency&gt;
</code></pre>

<p>application.yml</p>

<pre><code>spring:
  jpa:
    show-sql: true
    generate-ddl: false
    hibernate:
      ddl-auto: none
    properties:
      hibernate:
        format_sql: true
        dialect: org.hibernate.spatial.dialect.mysql.MySQL8SpatialDialect
</code></pre>

### Answer ID: 43010676
<p>I was using Hibernate-{core,spatial} v5.2.9 everything was as is above, except from how dialect was being set in <code>application.properties</code>. I <strong>NEEDED</strong>:</p>

<p><code>spring.jpa.database-platform=org.hibernate.spatial.dialect.postgis.PostgisDialect</code></p>

<p>Now it works. I don't need even any @Column annotation in my Entity.</p>

### Answer ID: 42671979
<p>I'm using Mysql 5 with <strong>Point</strong> object and had the same issue. 
The was with the newest dialect version, so I downgraded it.
Changing the <strong>aplication.properties</strong> from this:</p>

<pre><code>spring.jpa.properties.hibernate.dialect=org.hibernate.spatial.dialect.mysql.MySQL56InnoDBSpatialDialect
spring.jpa.database-platform = org.hibernate.spatial.dialect.mysql.MySQLSpatial56Dialect
</code></pre>

<p>To this:</p>

<pre><code>spring.jpa.properties.hibernate.dialect=org.hibernate.spatial.dialect.mysql.MySQL5InnoDBSpatialDialect
spring.jpa.database-platform = org.hibernate.spatial.dialect.mysql.MySQLSpatial56Dialect
</code></pre>

<p>I hope it can help you.</p>

### Answer ID: 40693087
<p>I would suggest using more generic approach, which is demonstrated in <a href="https://stackoverflow.com/a/27508639/2139804">this answer</a>. For me installing database extensions/ operating with geometrical types for such a simple type as Point is an overkill. </p>

### Answer ID: 40375731
<p>You have everything setup correctly for Postgresql + Postgis, but your database uses the Postgresql geometric types, not the ones provided by Postgis. Hibernate Spatial only supports the Postgis spatial extension.</p>

<p>Make sure Postgis is installed, and your tables uses the Postgis provided type 'Geometry' for the location column.</p>


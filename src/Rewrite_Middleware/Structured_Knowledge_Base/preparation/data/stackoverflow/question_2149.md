# JPA Subquery does not work in Criteria API
[Link to question](https://stackoverflow.com/questions/20728461/jpa-subquery-does-not-work-in-criteria-api)
**Creation Date:** 1387708575
**Score:** 0
**Tags:** java, mysql, sql, hibernate, jpa
## Question Body
<p>I'm learning Criteria API. I am trying to rewrite all my JPQL queries to Criteria API queries.</p>

<p>I use sakila database (<a href="http://dev.mysql.com/doc/sakila/en/%20SakilaDB" rel="nofollow">http://dev.mysql.com/doc/sakila/en/</a>), MySQL database and HibernatePersistence JPA provider.</p>

<p>I have got stuck in rewriting following query:</p>

<pre><code>SELECT c FROM Customer c 
JOIN c.addressId a 
JOIN a.cityId ct 
WHERE ct.countryId IN (SELECT co FROM Country co WHERE co.country = 'Germany')
</code></pre>

<p>It works fine, but the same in Criteria API doesn't work:</p>

<pre><code>CriteriaBuilder cb = em.getCriteriaBuilder();
CriteriaQuery&lt;Customer&gt; c = cb.createQuery(Customer.class);     
Root&lt;Customer&gt; cust = c.from(Customer.class);
Join&lt;Customer, Address&gt; address = cust.join(Customer_.addressId);
Join&lt;Address, City&gt; city = address.join(Address_.cityId);

Subquery&lt;Country&gt; sq = c.subquery(Country.class);
Root&lt;Country&gt; country = sq.from(Country.class);
sq.select(country).where(cb.equal(country.get(Country_.country), "Germany"));
c.where(cb.in(city.get(City_.countryId)).value(country));
</code></pre>

<p>I have got the following exception:</p>

<pre><code>javax.persistence.PersistenceException: org.hibernate.exception.SQLGrammarException: could not extract ResultSet
    at org.hibernate.ejb.AbstractEntityManagerImpl.convert(AbstractEntityManagerImpl.java:1387)
    at org.hibernate.ejb.AbstractEntityManagerImpl.convert(AbstractEntityManagerImpl.java:1310)
    at org.hibernate.ejb.QueryImpl.getResultList(QueryImpl.java:277)
    at org.hibernate.ejb.criteria.CriteriaQueryCompiler$3.getResultList(CriteriaQueryCompiler.java:254)
    at net.bean.java.sakila.test.SakilaQueries.inTest(SakilaQueries.java:100)
    at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
    at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:39)
    at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:25)
    at java.lang.reflect.Method.invoke(Method.java:597)
    at org.junit.runners.model.FrameworkMethod$1.runReflectiveCall(FrameworkMethod.java:47)
    at org.junit.internal.runners.model.ReflectiveCallable.run(ReflectiveCallable.java:12)
    at org.junit.runners.model.FrameworkMethod.invokeExplosively(FrameworkMethod.java:44)
    at org.junit.internal.runners.statements.InvokeMethod.evaluate(InvokeMethod.java:17)
    at org.junit.internal.runners.statements.RunBefores.evaluate(RunBefores.java:26)
    at org.junit.internal.runners.statements.RunAfters.evaluate(RunAfters.java:27)
    at org.junit.runners.ParentRunner.runLeaf(ParentRunner.java:271)
    at org.junit.runners.BlockJUnit4ClassRunner.runChild(BlockJUnit4ClassRunner.java:70)
    at org.junit.runners.BlockJUnit4ClassRunner.runChild(BlockJUnit4ClassRunner.java:50)
    at org.junit.runners.ParentRunner$3.run(ParentRunner.java:238)
    at org.junit.runners.ParentRunner$1.schedule(ParentRunner.java:63)
    at org.junit.runners.ParentRunner.runChildren(ParentRunner.java:236)
    at org.junit.runners.ParentRunner.access$000(ParentRunner.java:53)
    at org.junit.runners.ParentRunner$2.evaluate(ParentRunner.java:229)
    at org.junit.internal.runners.statements.RunBefores.evaluate(RunBefores.java:26)
    at org.junit.internal.runners.statements.RunAfters.evaluate(RunAfters.java:27)
    at org.junit.runners.ParentRunner.run(ParentRunner.java:309)
    at org.eclipse.jdt.internal.junit4.runner.JUnit4TestReference.run(JUnit4TestReference.java:50)
    at org.eclipse.jdt.internal.junit.runner.TestExecution.run(TestExecution.java:38)
    at org.eclipse.jdt.internal.junit.runner.RemoteTestRunner.runTests(RemoteTestRunner.java:467)
    at org.eclipse.jdt.internal.junit.runner.RemoteTestRunner.runTests(RemoteTestRunner.java:683)
    at org.eclipse.jdt.internal.junit.runner.RemoteTestRunner.run(RemoteTestRunner.java:390)
    at org.eclipse.jdt.internal.junit.runner.RemoteTestRunner.main(RemoteTestRunner.java:197)
Caused by: org.hibernate.exception.SQLGrammarException: could not extract ResultSet
    at org.hibernate.exception.internal.SQLExceptionTypeDelegate.convert(SQLExceptionTypeDelegate.java:82)
    at org.hibernate.exception.internal.StandardSQLExceptionConverter.convert(StandardSQLExceptionConverter.java:49)
    at org.hibernate.engine.jdbc.spi.SqlExceptionHelper.convert(SqlExceptionHelper.java:125)
    at org.hibernate.engine.jdbc.spi.SqlExceptionHelper.convert(SqlExceptionHelper.java:110)
    at org.hibernate.engine.jdbc.internal.ResultSetReturnImpl.extract(ResultSetReturnImpl.java:88)
    at org.hibernate.loader.Loader.getResultSet(Loader.java:2062)
    at org.hibernate.loader.Loader.executeQueryStatement(Loader.java:1859)
    at org.hibernate.loader.Loader.executeQueryStatement(Loader.java:1838)
    at org.hibernate.loader.Loader.doQuery(Loader.java:906)
    at org.hibernate.loader.Loader.doQueryAndInitializeNonLazyCollections(Loader.java:348)
    at org.hibernate.loader.Loader.doList(Loader.java:2548)
    at org.hibernate.loader.Loader.doList(Loader.java:2534)
    at org.hibernate.loader.Loader.listIgnoreQueryCache(Loader.java:2364)
    at org.hibernate.loader.Loader.list(Loader.java:2359)
    at org.hibernate.loader.hql.QueryLoader.list(QueryLoader.java:495)
    at org.hibernate.hql.internal.ast.QueryTranslatorImpl.list(QueryTranslatorImpl.java:357)
    at org.hibernate.engine.query.spi.HQLQueryPlan.performList(HQLQueryPlan.java:195)
    at org.hibernate.internal.SessionImpl.list(SessionImpl.java:1194)
    at org.hibernate.internal.QueryImpl.list(QueryImpl.java:101)
    at org.hibernate.ejb.QueryImpl.getResultList(QueryImpl.java:268)
    ... 29 more
Caused by: com.mysql.jdbc.exceptions.jdbc4.MySQLSyntaxErrorException: Unknown column 'generatedAlias3' in 'where clause'
    at sun.reflect.NativeConstructorAccessorImpl.newInstance0(Native Method)
    at sun.reflect.NativeConstructorAccessorImpl.newInstance(NativeConstructorAccessorImpl.java:39)
    at sun.reflect.DelegatingConstructorAccessorImpl.newInstance(DelegatingConstructorAccessorImpl.java:27)
    at java.lang.reflect.Constructor.newInstance(Constructor.java:513)
    at com.mysql.jdbc.Util.handleNewInstance(Util.java:411)
    at com.mysql.jdbc.Util.getInstance(Util.java:386)
    at com.mysql.jdbc.SQLError.createSQLException(SQLError.java:1054)
    at com.mysql.jdbc.MysqlIO.checkErrorPacket(MysqlIO.java:4237)
    at com.mysql.jdbc.MysqlIO.checkErrorPacket(MysqlIO.java:4169)
    at com.mysql.jdbc.MysqlIO.sendCommand(MysqlIO.java:2617)
    at com.mysql.jdbc.MysqlIO.sqlQueryDirect(MysqlIO.java:2778)
    at com.mysql.jdbc.ConnectionImpl.execSQL(ConnectionImpl.java:2825)
    at com.mysql.jdbc.PreparedStatement.executeInternal(PreparedStatement.java:2156)
    at com.mysql.jdbc.PreparedStatement.executeQuery(PreparedStatement.java:2323)
    at org.hibernate.engine.jdbc.internal.ResultSetReturnImpl.extract(ResultSetReturnImpl.java:79)
    ... 44 more
</code></pre>

<p>The query which is produced by Hibernate looks like:</p>

<pre><code>select 
customer0_.customer_id as customer1_5_, 
customer0_.active as active2_5_, 
customer0_.address_id as address_8_5_, 
customer0_.create_date as create_d3_5_, 
customer0_.email as email4_5_, 
customer0_.first_name as first_na5_5_, 
customer0_.last_name as last_nam6_5_, 
customer0_.last_update as last_upd7_5_, 
customer0_.store_id as store_id9_5_ 

from customer customer0_ 
inner join address address1_ on customer0_.address_id=address1_.address_id 
inner join city city2_ on address1_.city_id=city2_.city_id 

where city2_.country_id=generatedAlias3;
</code></pre>

<p>Thank you in advance.</p>

